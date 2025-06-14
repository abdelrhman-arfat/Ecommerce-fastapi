from fastapi import APIRouter, Response
from service.user_service import User_Service, VLoginUser, VRegisterUser
from service.response_service import response_service
from utils.try_catch_handler import try_catch_handler
from utils.jwt import Jwt
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_users():
    users = try_catch_handler(lambda: User_Service.get_all_users())
    return response_service.get_success_response(data=users, message="users fetched successfully")


@router.get("/active")
async def read_active_users():
    users = try_catch_handler(lambda: User_Service.get_all_active_users())
    return response_service.get_success_response(data=users, message="users fetched successfully")


@router.get("/non-active")
async def read_non_active_users():
    users = try_catch_handler(lambda: User_Service.get_all_non_active_users())
    return response_service.get_success_response(data=users, message="users fetched successfully")


@router.post("/login")
async def login_user(UserLogin: VLoginUser):
    data: dict = try_catch_handler(lambda: User_Service.user_login(UserLogin))
    user: dict = data["data"]
    message = data["message"]
    code = data["code"]
    if user is None:
        return response_service.get_error_response(data=None, message=message, status_code=code)

    token = try_catch_handler(
        lambda: Jwt.create_token({"id": str(user["id"])}, expire_time=1))
    print("token ------------>", token)
    response: Response = response_service.get_success_response(
        data=user, message=message)
    response = response_service.update_response_with_cookies(
        response=response, value=token)

    return response


@router.post("/register")
async def register_user(UserRegister: VRegisterUser):
    data: dict = try_catch_handler(
        lambda: User_Service.register_user(UserRegister))
    user = data["data"]
    message = data["message"]
    code = data["code"]
    if user is None:
        return response_service.get_error_response(data=None, message=message, status_code=code)
    token = try_catch_handler(
        lambda: Jwt.create_token({"id": str(user["id"])}, expire_time=1))
    response: Response = response_service.get_success_response(
        data=user, message=message)
    response_service.update_response_with_cookies(
        response=response, value=token)

    return response
