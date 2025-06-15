from fastapi import Response, Request
from fastapi.responses import JSONResponse


class response_service:
    @staticmethod
    def return_content(status_code=200, message="Success", data=None) -> dict:
        return {"status_code": status_code, "message": message, "data": data}

    @staticmethod
    def return_response(status_code=200, message="Success", data=None) -> Response:
        content = response_service.return_content(
            status_code=status_code, message=message, data=data)
        response = JSONResponse(content=content, status_code=status_code)
        return response

    @staticmethod
    def get_success_response(status_code=200, message="Success", data=None) -> Response:
        response = response_service.return_response(
            status_code=status_code, message=message, data=data)
        return response

    @staticmethod
    def get_error_response(status_code=400, message="Error", data=None) -> Response:
        response = response_service.return_response(
            status_code=status_code, message=message, data=data)
        return response

    @staticmethod
    def get_request_cookie(request: Request, key="token") -> str:
        return request.cookies.get(key)

    @staticmethod
    def update_response_with_cookies(response: Response, value, key="token", samesite="lax", httponly=True, secure=True):
        response.set_cookie(
            key=key,
            value=value,
            httponly=httponly,
            secure=secure,
            samesite=samesite,
        )

    @staticmethod
    def delete_response_cookies(response: Response, keys=["token", "refresh_token"], status_code=200, message="Success", data=None):
        if keys is None:
            keys = ["token", "refresh_token"]
        content = response_service.return_content(
            status_code=status_code,
            message=message,
            data=data
        )
        response = JSONResponse(content=content, status_code=status_code)
        for key in keys:
            response.delete_cookie(key=key)

        return response
