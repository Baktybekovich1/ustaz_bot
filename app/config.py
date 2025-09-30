import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_IDS = [int(x) for x in os.getenv("ADMIN_CHAT_IDS","").split(",") if x.strip()]
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_DSN = os.getenv("REDIS_DSN", "redis://redis:6379/0")
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
SERVICE_HOST = os.getenv("SERVICE_HOST", "0.0.0.0")
SERVICE_PORT = int(os.getenv("SERVICE_PORT", 8000))
