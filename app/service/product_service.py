from db.db_connection import engine
from sqlmodel import Session, select
from models.models import Product
from utils.to_JSON import to_JSON, return_code_data_message
from pydantic import BaseModel, Field
from fastapi import File, UploadFile, Form
from typing import Optional
from utils.Cloudinary_handler import Cloudinary_handler


class VCreateProduct:
    def __init__(
        self,
        name: str = Form(max_length=30),
        description: str = Form(max_length=100),
        price: float = Form(...),
        quantity: int = Form(...),
        image: UploadFile = File(...),
        category: str = Form(...),
        is_active: str = Form("true")

    ):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.image = image
        self.category = category
        self.is_active = is_active.lower() == "true" if True else False


class VUpdateProduct(BaseModel):
    name: Optional[str] = Field(max_length=30)
    description: Optional[str] = Field(max_length=100)
    price: Optional[float]
    quantity: Optional[int]


class Product_service:
    @staticmethod
    def is_product_exists(product_id, session):
        stmt = select(Product).where(Product.id == product_id)
        result = session.exec(stmt).first()
        return result

    @staticmethod
    def get_all_products():
        with Session(engine) as session:
            results = session.exec(select(Product)).all()
            return to_JSON(results)

    @staticmethod
    def get_product_by_id(product_id: int):
        with Session(engine) as session:
            stmt = select(Product).where(Product.id == product_id)
            result = session.exec(stmt).first()
            return to_JSON(result)

    @staticmethod
    def get_products_by_price_range(min_price: float, max_price: float):
        with Session(engine) as session:
            stmt = select(Product).where(
                Product.price.between(min_price, max_price))
            results = session.exec(stmt).all().order_by(Product.price)
            return to_JSON(results)

    @staticmethod
    def get_products_by_category(category: str):
        with Session(engine) as session:
            stmt = select(Product).where(Product.category == category)
            results = session.exec(stmt).all()
            return to_JSON(results)

    @staticmethod
    def get_products_by_name(name: str):
        with Session(engine) as session:
            stmt = select(Product).where(Product.name.startswith(name))
            results = session.exec(stmt).all()
            return to_JSON(results)

    @staticmethod
    def add_new_product(product_data: Product):
        with Session(engine) as session:
            new_product = Product(
                name=product_data.name,
                description=product_data.description,
                price=product_data.price,
                quantity=product_data.quantity,
                image=product_data.image,
                category=product_data.category,
                is_active=product_data.is_active
            )
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
        return to_JSON(new_product)

    @staticmethod
    def update_product(product_id: int, product_data: Product):
        with Session(engine) as session:
            db_product = Product_service.is_product_exists(product_id, session)
            if not db_product:
                return return_code_data_message("Product not found", None, 404)

            db_product.name = product_data.name or db_product.name
            db_product.price = product_data.price or db_product.price
            db_product.description = product_data.description or db_product.description
            db_product.quantity = product_data.quantity or db_product.quantity

            session.commit()
            session.refresh(db_product)
            return return_code_data_message("Product updated successfully", to_JSON(db_product), 200)

    @staticmethod
    async def delete_product(product_id: int):
        with Session(engine) as session:
            db_product = Product_service.is_product_exists(product_id, session)
            if db_product is None:
                return return_code_data_message("Product not found", None, 404)
            # ** --> For best practices make func delete the image from the Cloudinary if you want but we don't need here because it learning project
            """ 
            cloudinary.delete_image(db_product.image) You can see it in the cloudinary.py
            """
            data = await Cloudinary_handler.delete_image(db_product.image)
            session.delete(db_product)
            session.commit()
            return return_code_data_message("Product deleted successfully",  to_JSON(db_product), code=200)

    @staticmethod
    def get_all_active_products():
        with Session(engine) as session:
            stmt = select(Product).where(Product.is_active == True)
            results = session.exec(stmt).all()
            return to_JSON(results)

    @staticmethod
    def get_all_non_active_products():
        with Session(engine) as session:
            stmt = select(Product).where(Product.is_active == False)
            results = session.exec(stmt).all()
            return to_JSON(results)
