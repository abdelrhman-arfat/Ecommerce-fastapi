
from dotenv import load_dotenv
import os

# Loading .evn file
load_dotenv()


class Constants:
    DB_URL = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    token = "token"
    refresh_token = "refresh_token"
