# SRE Notifier Tool

The **SRE Notifier Tool** is designed to automate communication with community members and node operators across multiple channels such as Discord, Slack, Telegram, and Status Pages. The tool simplifies and centralizes the process of notifying your community about network updates, outages, security patches, and other important events.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Running in Docker](#running-in-docker)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features
- Send upgrade or incident notifications to:
  - **Discord** using webhooks
  - **Slack** using webhooks
  - **Telegram** via the Telegram Bot API
- Configurable and extendable

## Prerequisites
- Python 3.8 or later
- Pip 
- Access to your Slack workspace, Discord server and Telegram bot

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/community-communicator-tool.git
   cd community-communicator-tool
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

# Configuration
1. Copy the sample configuration file and adjust it to your needs:
   ```bash
   cp config/config.example.yaml config/config.yaml
   ```
2. Update config.yaml with your credentials and settings:

   ```yaml
   vault:
     address: "http://127.0.0.1:8200"
     token: "s.YOUR_VAULT_TOKEN"
   
   slack:
     webhook_url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
   
   discord:
     webhook_url: "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"
   
   telegram:
     bot_token: "YOUR_TELEGRAM_BOT_API_TOKEN"
     chat_id: "YOUR_CHAT_ID"
   ```
# Usage
You can run the application using the main.py script.

   ```bash
   python src/main.py
   ```
For example, sending a test message via Slack:

   ```python
   from src.slack_notifier import SlackNotifier
   notifier = SlackNotifier(webhook_url="YOUR_SLACK_WEBHOOK_URL")
   notifier.send_message(message="Hello from the SRE Notifier Tool!")
   ```
# Running in Docker
1. Build the Docker image:

   ```bash
   docker build -t community-communicator .
   ```
2. Run the container:

   ```bash
   docker run --rm -v $(pwd)/config:/app/config community-communicator
   ```
# Testing
1. Install the testing requirements:

   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run the tests using pytest:

   ```bash
   pytest tests/
   ```

Contributing
We welcome contributions! Please follow these steps to contribute:

Fork the repository
Create a new branch (git checkout -b feature/your-feature-name)
Commit your changes (git commit -m 'Add some feature')
Push to the branch (git push origin feature/your-feature-name)
Create a pull request

