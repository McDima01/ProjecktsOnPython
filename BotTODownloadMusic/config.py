import os

# CHANNEL_ID = "@skndaas" #skndaas | UnLocal_Music_Dima
BOT_TOKEN = os.getenv("BOT_TOKEN")
PAYMENT_PROVIDER_BOT_TOKEN = ""
YANDEX_TOKEN = os.getenv("YANDEX_TOKEN")
DATA_FILE = "user_data.json"

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
