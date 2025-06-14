import jwt
from datetime import datetime, timedelta, timezone
from utils.Constants import Constants


class Jwt:
    @staticmethod
    def create_token(data: dict, expire_time: int = 1) -> str:
        to_encode = data.copy()
        expires_delta = timedelta(hours=expire_time)
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            Constants.JWT_SECRET_KEY,
            algorithm="HS256"
        )
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> dict:

        try:
            payload = jwt.decode(
                token,
                Constants.JWT_SECRET_KEY,
                algorithms=["HS256"],
                options={"verify_exp": True}
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token expired")
        except jwt.InvalidTokenError as e:
            raise Exception(f"Invalid token: {str(e)}")

    @staticmethod
    def encode_token(data: dict) -> str:
        return Jwt.create_token(data)
