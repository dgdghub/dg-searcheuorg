
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TG_TOKEN = os.getenv('TG_TOKEN')
    TG_CHAT_ID = os.getenv('TG_CHAT_ID')

