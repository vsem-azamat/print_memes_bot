from bestconfig import Config
from pydantic import BaseSettings, SecretStr

config = Config()

class Settings(BaseSettings):
    bot_token: SecretStr = config['BOT_TOKEN']
    admins: list[int] = config['ADMINS']

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'

settings = Settings()