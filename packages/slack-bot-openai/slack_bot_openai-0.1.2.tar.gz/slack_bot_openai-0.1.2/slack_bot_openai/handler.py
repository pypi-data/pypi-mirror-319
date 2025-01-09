import json
import os
import logging
import time
import re
from openai import OpenAI
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from typing import Dict, List
import boto3
from datetime import datetime, timedelta

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class SlackBotHandler:
    def __init__(self, system_message: str, model: str = 'gpt-4o', include_chat_history: bool = True):
        # Environment setup and validation
        self.slack_bot_token = os.getenv('SLACK_BOT_TOKEN')
        self.slack_signing_secret = os.getenv('SLACK_SIGNING_SECRET')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.openai_base_url = os.getenv('OPENAI_BASE_URL')
        self.openai_model = os.getenv('OPENAI_MODEL', model)
        self.include_chat_history = os.getenv('INCLUDE_CHAT_HISTORY', str(include_chat_history)).lower() == 'true'
        self.dynamodb_table = os.getenv('DYNAMODB_TABLE', 'slack-bot-processed-messages')
        self.system_message = system_message

        if not self.slack_bot_token:
            raise ValueError("SLACK_BOT_TOKEN environment variable is not set")
        if not self.slack_signing_secret:
            raise ValueError("SLACK_SIGNING_SECRET environment variable is not set")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        # Initialize DynamoDB
        self.dynamodb = boto3.resource('dynamodb')
        self.message_table = self.dynamodb.Table(self.dynamodb_table)

        # Initialize the Bolt app
        self.app = App(
            process_before_response=True,
            token=self.slack_bot_token,
            signing_secret=self.slack_signing_secret
        )

        # Set up event handlers
        self.app.event("message")(self.handle_all_messages)
        self.app.event("app_mention")(self.handle_app_mention)

    def is_message_processed(self, client_msg_id: str) -> bool:
        """Check if a message has already been processed"""
        if not client_msg_id:
            return False
            
        try:
            response = self.message_table.get_item(
                Key={'client_msg_id': client_msg_id}
            )
            return 'Item' in response
        except Exception as e:
            logger.error(f"Error checking message status: {str(e)}")
            return False

    def mark_message_processed(self, client_msg_id: str):
        """Mark a message as processed"""
        if not client_msg_id:
            return
            
        try:
            # Store with TTL of 24 hours
            ttl = int((datetime.now() + timedelta(hours=24)).timestamp())
            self.message_table.put_item(
                Item={
                    'client_msg_id': client_msg_id,
                    'processed_at': datetime.now().isoformat(),
                    'ttl': ttl
                }
            )
        except Exception as e:
            logger.error(f"Error marking message as processed: {str(e)}")

    def process_chat_completion(self, messages: List[Dict], temperature: float = 0.7,
                              max_tokens: int = 500, top_p: float = 1,
                              frequency_penalty: float = 0, presence_penalty: float = 0) -> Dict:
        """Process chat completion using OpenAI"""
        try:
            # Initialize OpenAI client with only supported parameters
            client_params = {
                "api_key": self.openai_api_key,
                **({"base_url": self.openai_base_url} if self.openai_base_url else {})
            }
                
            client = OpenAI(**client_params)
            completion_params = {
                "model": self.openai_model,
                "messages": messages,
                "temperature": temperature,
                "top_p": top_p,
                "frequency_penalty": frequency_penalty,
                "presence_penalty": presence_penalty,
            }
            if max_tokens:
                completion_params["max_tokens"] = max_tokens

            logger.debug(f"Using model: {self.openai_model}")
            logger.debug(f"Base URL: {self.openai_base_url if self.openai_base_url else 'default'}")
            logger.debug(f"Number of messages: {len(messages)}")

            try:
                response = client.chat.completions.create(**completion_params)
                message = response.choices[0].message
                
                result = {
                    "answer": {
                        "role": message.role,
                        "content": message.content,
                        "tool_calls": message.function_call if hasattr(message, 'function_call') else None
                    }
                }
                return result

            except Exception as api_error:
                logger.error("OpenAI API Error")
                logger.error(f"Type: {type(api_error)}")
                logger.error(f"Message: {str(api_error)}")
                logger.error(f"Model: {self.openai_model}")
                logger.error(f"Base URL: {self.openai_base_url}")
                raise

        except Exception as e:
            logger.error("Error in process_chat_completion", exc_info=True)
            logger.error(f"System message: {self.system_message[:100]}...")
            raise

    def get_conversation_history(self, client, channel_id: str, event: Dict) -> List[Dict]:
        """Get conversation history based on context (DM or thread)."""
        try:
            is_in_dm_with_bot = event.get("channel_type") == "im"
            thread_ts = event.get("thread_ts")
            messages_in_context = []

            if thread_ts:
                # Within a thread - get only messages from this thread
                result = client.conversations_replies(
                    channel=channel_id,
                    ts=thread_ts,
                    include_all_metadata=True,
                    limit=100,
                )
                messages_in_context = result.get("messages", [])
                
            elif is_in_dm_with_bot:
                # In DM with bot, not in a thread
                result = client.conversations_history(
                    channel=channel_id,
                    include_all_metadata=True,
                    limit=100,
                )
                messages = result.get("messages", [])
                
                # Filter messages from last 24 hours
                current_time = time.time()
                for message in messages:
                    seconds = current_time - float(message.get("ts", 0))
                    if seconds < 86400:  # less than 1 day
                        messages_in_context.append(message)
                
                # Reverse to get oldest first
                messages_in_context.reverse()
            
            # Filter out deleted messages and messages from other bots
            active_messages = [
                msg for msg in messages_in_context 
                if (
                    msg.get("subtype") != "message_deleted" and
                    msg.get("hidden", False) == False
                )
            ]
            
            return active_messages
        except Exception as e:
            logger.error(f"Error fetching conversation history: {str(e)}")
            return []

    def format_history_for_openai(self, messages: List[Dict], bot_id: str) -> List[Dict]:
        """Format Slack messages for OpenAI context"""
        formatted_messages = []
        for msg in messages:
            # Strip bot mention from initial message if present
            text = msg.get('text', '')
            if bot_id:
                text = re.sub(f"<@{bot_id}>\\s*", "", text)
                
            if msg.get('bot_id'):  # Bot's message
                formatted_messages.append({
                    "role": "assistant",
                    "content": text
                })
            else:  # User's message
                formatted_messages.append({
                    "role": "user",
                    "content": text
                })
        return formatted_messages

    def delete_conversation_history(self, client, channel_id: str) -> bool:
        """Delete all messages from the conversation history, including threads"""
        try:
            # Get all messages
            result = client.conversations_history(
                channel=channel_id,
                limit=1000  # Maximum allowed
            )
            messages = result.get('messages', [])
            
            deleted_count = 0
            for msg in messages:
                try:
                    # Check if message has replies
                    if msg.get('thread_ts'):
                        # Get thread messages
                        thread_result = client.conversations_replies(
                            channel=channel_id,
                            ts=msg['thread_ts']
                        )
                        thread_messages = thread_result.get('messages', [])
                        
                        # Delete bot messages in thread
                        for thread_msg in thread_messages:
                            if thread_msg.get('bot_id'):
                                try:
                                    client.chat_delete(
                                        channel=channel_id,
                                        ts=thread_msg['ts']
                                    )
                                    deleted_count += 1
                                except Exception as thread_del_error:
                                    logger.error(f"Failed to delete thread message {thread_msg.get('ts')}: {str(thread_del_error)}")
                                    continue
                    
                    # Delete main message if it's from bot
                    if msg.get('bot_id'):
                        client.chat_delete(
                            channel=channel_id,
                            ts=msg['ts']
                        )
                        deleted_count += 1
                except Exception as del_error:
                    logger.error(f"Failed to delete message {msg.get('ts')}: {str(del_error)}")
                    continue
            
            logger.info(f"Deleted {deleted_count} messages from conversation history (including threads)")
            return True
        except Exception as e:
            logger.error(f"Error deleting conversation history: {str(e)}")
            return False

    def should_ignore_message(self, event: Dict, client) -> bool:
        """Determine if a message should be ignored based on its properties."""
        # Ignore bot messages
        if event.get("bot_id"):
            return True
            
        channel_type = event.get("channel_type")
        thread_ts = event.get("thread_ts")
        
        # For DMs, process all non-bot messages
        if channel_type == "im":
            return False
        
        # For threads, check if the thread was started with the bot
        if thread_ts:
            try:
                # Get the parent message of the thread
                result = client.conversations_replies(
                    channel=event.get("channel"),
                    ts=thread_ts,
                    limit=1  # We only need the first message
                )
                if result.get("messages"):
                    parent_message = result["messages"][0]
                    # Process if the thread's first message mentions the bot
                    bot_user_id = self.app.client.auth_test()["user_id"]
                    return f"<@{bot_user_id}>" not in parent_message.get("text", "")
            except Exception as e:
                logger.error(f"Error checking thread parent: {str(e)}")
                return True
        
        # Ignore non-DM channel messages
        if channel_type != "im":
            return True
        
        return False

    def handle_message(self, body: Dict, say, logger, client, is_mention: bool = False):
        """Common handler for all message types"""
        try:
            # Get message details
            event = body["event"]
            client_msg_id = event.get("client_msg_id")
            
            # Skip if no client_msg_id
            if not client_msg_id:
                return
            
            channel_id = event.get("channel")
            channel_type = event.get("channel_type")
            thread_ts = event.get("thread_ts", event.get("ts"))
            text = event.get("text", "").strip()
            
            # Check for duplicate message
            if self.is_message_processed(client_msg_id):
                return
            
            # Mark message as processed immediately to prevent duplicates
            self.mark_message_processed(client_msg_id)
            
            # Ignore bot messages
            if body.get("event", {}).get("bot_id"):
                return
                
            # For mentions, remove the bot user mention from the text
            if is_mention:
                text = text.split(">", 1)[1].strip() if ">" in text else text
            
            if not text:
                return
                
            # Handle special command for deleting history
            if channel_type == "im" and text.lower() == "delete all history":
                self.delete_conversation_history(client, channel_id)
                return
            
            # Prepare messages for OpenAI
            messages = [{"role": "system", "content": self.system_message}]
            
            # Get conversation history for DMs and threads
            if (channel_type == "im" and self.include_chat_history) or thread_ts:
                history = self.get_conversation_history(client, channel_id, event)
                # Remove the current message from history if it exists
                history = [msg for msg in history if msg.get('ts') != event.get('ts')]
                formatted_history = self.format_history_for_openai(history, body.get("authorizations", [{}])[0].get("user_id"))
                messages.extend(formatted_history)
            
            # Add the current message
            messages.append({"role": "user", "content": text})

            # Call OpenAI for response
            try:
                response = self.process_chat_completion(
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500
                )
                
                # Send response back to Slack
                if response and response.get('answer'):
                    content = response['answer'].get('content', '')
                    # Only use thread_ts for non-DM channels
                    thread = thread_ts if channel_type != "im" else None
                    say(
                        text=content,
                        thread_ts=thread,
                        channel=channel_id
                    )
                else:
                    raise ValueError("No valid response content from OpenAI")
                    
            except Exception as e:
                logger.error(f"Error during OpenAI call: {str(e)}")
                raise
                
        except Exception as e:
            logger.error("Error processing message", exc_info=True)
            try:
                # Only use thread_ts for non-DM channels
                thread = thread_ts if channel_type != "im" else None
                error_message = "Sorry, I encountered an error. Please check if the OpenAI model and API settings are correct."
                if "model_not_found" in str(e).lower():
                    error_message = f"Error: The model '{self.openai_model}' was not found. Please check your model configuration."
                elif "invalid_api_key" in str(e).lower():
                    error_message = "Error: Invalid OpenAI API key. Please check your API key configuration."
                say(
                    text=error_message,
                    thread_ts=thread,
                    channel=channel_id
                )
            except Exception as say_error:
                logger.error(f"Failed to send error message to Slack: {str(say_error)}")

    def handle_all_messages(self, ack, body, say, logger, client):
        """Handle direct messages (DMs) and thread messages to the bot."""
        # Acknowledge receipt immediately
        ack()
        
        event = body["event"]
        
        # Early returns for messages we should ignore
        if self.should_ignore_message(event, client):
            return
            
        # Process both DMs and thread messages
        self.handle_message(body, say, logger, client)

    def handle_app_mention(self, ack, body, say, logger, client):
        """Handle when the bot is mentioned in channels"""
        # Acknowledge receipt immediately
        ack()
        
        event = body["event"]
        self.handle_message(body, say, logger, client, is_mention=True)

    def get_lambda_handler(self):
        """Get the Lambda handler for AWS Lambda deployment"""
        handler = SlackRequestHandler(app=self.app)
        
        def lambda_handler(event: Dict, context) -> Dict:
            """AWS Lambda handler"""
            try:
                response = handler.handle(event, context)
                # Ensure we return a proper response structure
                if isinstance(response, dict) and 'statusCode' in response:
                    return response
                else:
                    return {
                        'statusCode': 200,
                        'body': json.dumps({'message': 'Success', 'response': response})
                    }
            except Exception as e:
                logger.error(f"Error in lambda_handler: {str(e)}", exc_info=True)
                return {
                    'statusCode': 500,
                    'body': json.dumps({'error': str(e)})
                }
                
        return lambda_handler 