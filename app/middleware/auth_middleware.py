from fastapi import Request, HTTPException
from service.response_service import response_service
from service.user_service import User_Service
from utils.Constants import Constants
from utils.jwt import Jwt
from utils.try_catch_handler import try_catch_handler
from utils.custom_http_exception import custom_http_exception


class auth_middleware:
    @staticmethod
    async def is_admin(request: Request):
        await auth_middleware.is_login(request=request)
        user = request.state.user
        if user["role"] != Constants.user_roles["admin"]:
            raise custom_http_exception(
                data=None,
                message="You are not admin and can't do this operation",
                status_code=403
            )

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

        user = try_catch_handler(
            lambda: User_Service.get_user_by_id(payload["user_id"]))

        if not user:
            raise custom_http_exception(
                data=None,
                message="You are not logged in",
                status_code=401
            )
        request.state.user = user
        return True
