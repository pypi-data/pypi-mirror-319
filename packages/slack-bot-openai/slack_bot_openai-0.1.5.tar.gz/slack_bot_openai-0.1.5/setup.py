from setuptools import setup, find_packages

setup(
    name="slack_bot_openai",
    version="0.1.5",
    description="OpenAI-powered Slack bot framework with conversation history and thread support",
    author="Bary Huang",
    author_email="buryhuang@gmail.com",
    packages=find_packages(),
    install_requires=[
        "openai==1.59.5",
        "slack-bolt>=1.18.0",
        "boto3==1.34.49"
    ],
    python_requires=">=3.11",
) 