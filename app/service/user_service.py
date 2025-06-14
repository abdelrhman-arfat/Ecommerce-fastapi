from sqlmodel import Session, select, column
from db.db_connection import engine
from pydantic import BaseModel
from models.models import User
from utils.Hasher import Hasher
from utils.to_JSON import to_JSON


class VLoginUser(BaseModel):
    email: str
    password: str


class VRegisterUser(BaseModel):
    name: str
    email: str
    password: str


class VUpdateUser(BaseModel):
    name: str
    password: str


BASE_USER_COLUMNS = (User.id, User.name, User.email, User.role)


class User_Service:
    @staticmethod
    def return_code_data_message(message, data=None, code=400):
        return {
            "message": message,
            "data": data,
            "code": code
        }

    @staticmethod
    def user_exists(email, session):
        stmt = select(User).where(User.email == email)
        result = session.exec(stmt).first()
        if result is None:
            return None

        return result

    @staticmethod
    def user_public_information(user: User):
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }

    @staticmethod
    def get_all_users():
        with Session(engine) as session:
            results = session.exec(select(User)).all()
            return to_JSON(results, exclude=["password"])

    @staticmethod
    def get_all_active_users():
        with Session(engine) as session:
            stmt = select(User).where(User.is_active ==
                                      True)
            result = session.exec(stmt).all()
            return to_JSON(result, exclude=["password"])

    @staticmethod
    def get_all_non_active_users():
        with Session(engine) as session:

            result = session.exec(select(User).where(User.is_active ==
                                                     False)).all()
            return to_JSON(result, exclude=["password"])

    @staticmethod
    def user_login(UserLogin: VLoginUser):
        with Session(engine) as session:
            user: User = User_Service.user_exists(UserLogin.email, session)
            if user is None:
                returnedMessage = User_Service.return_code_data_message(
                    "User not found", None, 404)
                return returnedMessage

            is_password_match = Hasher.verify_password(UserLogin.password,
                                                       user.password)
            if not is_password_match:
                returnedMessage = User_Service.return_code_data_message(
                    "Invalid Credentials", None, 400
                )
                return returnedMessage
            userResponse = User_Service.user_public_information(user)
            returnedMessage = User_Service.return_code_data_message(
                "Login Successfully", userResponse, 200
            )
            return returnedMessage

    @staticmethod
    def register_user(UserRegister: VRegisterUser):
        with Session(engine) as session:
            user = User_Service.user_exists(UserRegister.email, session)
            if user is not None:
                returnedMessage = User_Service.return_code_data_message(
                    "User already exists Please try another email", None, 400
                )
                return returnedMessage
            hashed_password = Hasher.get_password_hash(
                UserRegister.password)
            user = User(
                name=UserRegister.name,
                email=UserRegister.email,
                password=hashed_password,
                is_active=True,
                role="user"
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            userResponse = User_Service.user_public_information(user)
            returnMessage = User_Service.return_code_data_message(
                "Registration Successfully", userResponse, 200
            )
            return returnMessage
