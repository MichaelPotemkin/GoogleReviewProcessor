import os

import pandas as pd
from amadeus import Client as AmadeusClient
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
    AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
    AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")
    MONARC_API_TOKEN = os.getenv("MONARC_API_TOKEN")
    MONARC_SOCKET_URL = os.getenv("MONARC_SOCKET_URL")
    TRAVECH_TECHNOLOGIES_UID = os.getenv("TRAVECH_TECHNOLOGIES_UID")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = os.getenv("SMTP_PORT")
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
    DATABASE_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    DATABASE_URL_SYNC = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    SECRET_KEY = "jfdsfljds"
    LOGGER_LEVEL = os.getenv("LOGGER_LEVEL", default="INFO")


settings = Settings()

amadeus_client = AmadeusClient(
    client_id=settings.AMADEUS_CLIENT_ID, client_secret=settings.AMADEUS_CLIENT_SECRET, hostname="production"
)
airports_dataframe = pd.read_excel("airports_with_ids.xlsx")
