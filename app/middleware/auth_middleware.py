from fastapi import Request, HTTPException
from service.response_service import response_service
from utils.Constants import Constants
from utils.jwt import Jwt
from utils.try_catch_handler import try_catch_handler
from utils.custom_http_exception import custom_http_exception


class auth_middleware:
    @staticmethod
    async def is_login(request: Request):
        token = try_catch_handler(lambda: response_service.get_request_cookie(
            request=request, key=Constants.token))

        if not token:
            raise custom_http_exception(
                data=None,
                message="You are not logged in",
                status_code=401
            )

        payload = try_catch_handler(lambda: Jwt.get_payload(token))
        if not payload:
            raise custom_http_exception(
                data=None,
                message="You are not logged in",
                status_code=401
            )

        request.state.user_id = payload["user_id"]
        return True
