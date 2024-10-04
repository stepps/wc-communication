import requests
import logging

class DiscordNotify:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.logger = logging.getLogger(__name__)

    def send_message(self, message: str, username: str = "Notifier Bot", embed_title: str = None):
        data = {
            "username": username,
            "content": message,
        }

        if embed_title:
            data["embeds"] = [{
                "title": embed_title,
                "description": message,
                "color": 3066993
            }]

        try:
            response = requests.post(self.webhook_url, json=data)
            response.raise_for_status()
            self.logger.info(f"Message Discord successfully: {message}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send message to Discord: {e}")
            raise

if __name__ == "__main__":
    DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1291603140570775646/JTu7auWky-8dxS8bFCXlg7LYc4HPxoweiiyq772kCFSOWfopOXIJFPMkr4tIvSiqSnGK"
    
    notifier = DiscordNotify(webhook_url=DISCORD_WEBHOOK_URL)
    notifier.send_message(
        message="Hello from the SRE team! This is a test notification.",
        username="ZetaChain SRE Notifier",
        embed_title="Network Status Update"
    )

