import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass
class Settings:
    BOT_TOKEN = str(os.getenv('BOT_TOKEN'))
    ADMINS = [int(id_admin) for id_admin in os.getenv('ADMINS').split(',')]

settings = Settings