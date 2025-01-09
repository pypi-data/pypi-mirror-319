# Slack Bot OpenAI

OpenAI integration for Slack bots with conversation history and thread support. This package provides shared functionality for handling Slack events with OpenAI integration and message processing.

## Installation

```bash
pip install slack_bot_openai
```

## Usage

```python
from slack_bot_openai.handler import SlackBotHandler

# Initialize the bot handler
bot_handler = SlackBotHandler(
    system_message="Your system message here",
    model="gpt-4o",  # or your preferred model
    include_chat_history=True
)

# Get the Lambda handler
lambda_handler = bot_handler.get_lambda_handler()
```

## Features

- Slack event handling with OpenAI integration
- Message history management
- DynamoDB integration for message deduplication
- Thread message support
- Configurable system messages and models

## Requirements

- Python 3.11+
- openai==1.53.0
- slack-bolt>=1.18.0
- boto3==1.34.49

## Environment Variables

The following environment variables are required:

- `SLACK_BOT_TOKEN`: Slack Bot User OAuth Token
- `SLACK_SIGNING_SECRET`: Slack Signing Secret
- `OPENAI_API_KEY`: OpenAI API Key

Optional environment variables:

- `OPENAI_BASE_URL`: Custom OpenAI API base URL
- `OPENAI_MODEL`: OpenAI model name (defaults to gpt-4o)
- `INCLUDE_CHAT_HISTORY`: Whether to include chat history (defaults to true)
- `DYNAMODB_TABLE`: DynamoDB table name for message deduplication
