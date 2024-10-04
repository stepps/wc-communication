import requests
import logging

class SlackNotify:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.logger = logging.getLogger(__name__)

    def send_message(self, message: str, username: str = "Notifier Bot", channel: str = None, icon_emoji: str = None, icon_url: str = None):
        data = {
            "text": message,
            "username": username
        }

        if channel:
            data["channel"] = channel

        if icon_emoji:
            data["icon_emoji"] = icon_emoji  # Adds an emoji as the message icon
        
        if icon_url:
            data["icon_url"] = icon_url

        try:
            response = requests.post(self.webhook_url, json=data)
            response.raise_for_status()
            self.logger.info(f"Message sent to Slack successfully: {message}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send message to Slack: {e}")
            raise

if __name__ == "__main__":

    SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"
    
    notifier = SlackNotify(webhook_url=SLACK_WEBHOOK_URL)
    notifier.send_message(
        message="Hello from the SRE team! This is a test notification.",
        username="ZetaChain SRE Notifier",
        channel="#general",
        icon_emoji=":robot_face:"
    )
