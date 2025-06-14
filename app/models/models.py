from sqlmodel import SQLModel, Field
from enum import Enum
from typing import Optional


class Role(str, Enum):
    user = "user"
    admin = "admin"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
    is_active: bool = Field(default=True)
    role: Role = Field(default=Role.user)


class Product(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    quantity: int
    image: str
    category: str
    is_active: bool


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    product_id: int = Field(default=None, foreign_key="product.id")
    quantity: int
    total_price: float


class Cart(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    product_id: int = Field(default=None, foreign_key="product.id")
    quantity: int


class PaymentUsedSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    order_id: int = Field(default=None, foreign_key="order.id")
    payment_id: str
