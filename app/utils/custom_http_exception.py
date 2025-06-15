from fastapi import HTTPException

class custom_http_exception(HTTPException):
    def __init__(self, status_code: int, message: str = "Error", data=None):
        super().__init__(status_code=status_code, detail={
            "status_code": status_code,
            "message": message,
            "data": data
        })