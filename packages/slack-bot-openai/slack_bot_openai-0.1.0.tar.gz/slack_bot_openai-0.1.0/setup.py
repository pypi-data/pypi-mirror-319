from setuptools import setup, find_packages

setup(
    name="slack_bot_openai",
    version="0.1.0",
    description="OpenAI integration for Peakmojo Slack bots",
    author="Peakmojo",
    author_email="dev@peakmojo.com",
    packages=find_packages(),
    install_requires=[
        "openai==1.53.0",
        "slack-bolt>=1.18.0",
        "boto3==1.34.49"
    ],
    python_requires=">=3.11",
) 