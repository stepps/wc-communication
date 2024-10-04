import requests
import logging

class TelegramNotify:
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize TelegramNotify with the bot token and chat ID.
        
        :param bot_token: Telegram Bot API token.
        :param chat_id: ID of the Telegram chat (group, channel, or user) to send messages to.
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.logger = logging.getLogger(__name__)
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_message(self, message: str, parse_mode: str = "Markdown", disable_web_page_preview: bool = False):
        """
        Send a message to the Telegram chat via the bot API.
        
        :param message: The content of the message to send.
        :param parse_mode: Optional formatting mode (e.g., "Markdown", "HTML").
        :param disable_web_page_preview: Set to True to disable link previews.
        :return: None
        """
        data = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_web_page_preview
        }

        try:
            response = requests.post(self.api_url, json=data)
            response.raise_for_status()
            self.logger.info(f"Message sent to Telegram successfully: {message}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send message to Telegram: {e}")
            raise

if __name__ == "__main__":
    TELEGRAM_BOT_TOKEN = "7368392863:AAHFUveUPw6JHOOrnkLsD26LDXuvtfXWO-0"
    TELEGRAM_CHAT_ID = "-1002299367785"

    notifier = TelegramNotify(bot_token=TELEGRAM_BOT_TOKEN, chat_id=TELEGRAM_CHAT_ID)
    notifier.send_message(
        message="Hello from the SRE team! This is a test notification via Telegram.",
        parse_mode="Markdown",  # Optional: Can be "Markdown", "HTML", or None
        disable_web_page_preview=True  # Optional: Set to True to avoid link previews
    )
