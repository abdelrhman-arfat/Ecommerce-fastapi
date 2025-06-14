from sqlmodel import SQLModel, create_engine
from utils.Constants import Constants
import asyncio
from models.models import User, Role, Product, Cart, Order, PaymentUsedSession

mysql_url = Constants.DB_URL
engine = create_engine(mysql_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    try:
        create_db_and_tables()
        print("✅ Tables created successfully")
    except Exception as e:
        print("❌ Error creating tables:", e)
