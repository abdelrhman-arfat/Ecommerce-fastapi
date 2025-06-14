
from dotenv import load_dotenv
import os

# Loading .evn file
load_dotenv()


class Constants:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES = 10080
    
    DB_URL = os.getenv("DATABASE_URL")
