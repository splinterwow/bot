from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))
MEDIA_CHANNEL_ID = int(os.getenv("MEDIA_CHANNEL_ID"))
WELCOME_VIDEO_ID = os.getenv("WELCOME_VIDEO_ID")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

PROXY_URL = os.getenv("PROXY_URL")
PROXY_USERNAME = os.getenv("PROXY_USERNAME")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")

POSITIONS = {
    "sales": "Sotuv menejeri",
    "smm": "SMM mutaxassisi",
    "copywriter": "Kopirayter",
    "volunteer": "Valantyor"
}
