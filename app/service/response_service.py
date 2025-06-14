from fastapi import Response
from fastapi.responses import JSONResponse


class response_service:
    @staticmethod
    def return_response(status_code=200, message="Success", data=None) -> Response:
        content = {"status_code": status_code,
                   "message": message, "data": data}
        response = JSONResponse(content=content, status_code=status_code)
        return response

    @staticmethod
    def get_error_response(status_code=400, message="Error", data=None) -> Response:
        response = response_service.return_response(
            status_code=status_code, message=message, data=data)
        return response

    @staticmethod
    def get_success_response(status_code=200, message="Success", data=None) -> Response:
        response = response_service.return_response(
            status_code=status_code, message=message, data=data)
        return response

    @staticmethod
    def update_response_with_cookies(response: Response, value, key="token", samesite="lax", httponly=True, secure=True) -> Response:
        response.set_cookie(
            key=key,
            value=value,
            httponly=httponly,
            secure=secure,
            samesite=samesite,
        )
        return response
