import jwt
from datetime import datetime, timedelta, timezone
from utils.Constants import Constants


class Jwt:
    @staticmethod
    def create_token(data: dict, expire_timedelta: timedelta = timedelta(days=7)) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expire_timedelta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            Constants.JWT_SECRET_KEY,
            algorithm="HS256"
        )
        return encoded_jwt

    @staticmethod
    def get_payload(token: str) -> dict:
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

    def is_verified(token: str) -> bool:
        try:
            Jwt.get_payload(token)
            return True
        except Exception as e:
            return False

    @staticmethod
    def encode_token(data: dict) -> str:
        return Jwt.create_token(data)
    
