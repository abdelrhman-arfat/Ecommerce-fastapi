from passlib.hash import pbkdf2_sha256


class Hasher():
    @staticmethod
    def verify_password(plain_password, hashed_password) -> str:
        return pbkdf2_sha256.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password) -> str:
        return pbkdf2_sha256.hash(password)
