from fastapi import APIRouter, Response, Request, Depends
from service.user_service import User_Service, VLoginUser, VRegisterUser
from service.response_service import response_service
from utils.Constants import Constants
from utils.try_catch_handler import try_catch_handler
from utils.jwt import Jwt
from utils.Date_token_handler import date_time_handler
from middleware.auth_middleware import auth_middleware
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# ------------------------------- Admin Operations ---------------------------------


@router.get("/")
async def read_users(_=Depends(auth_middleware.is_login)):
    users = try_catch_handler(lambda: User_Service.get_all_users())
    return response_service.get_success_response(data=users, message="users fetched successfully")


@router.get("/active")
async def read_active_users(_=Depends(auth_middleware.is_login)):
    users = try_catch_handler(lambda: User_Service.get_all_active_users())
    return response_service.get_success_response(data=users, message="users fetched successfully")


@router.get("/non-active")
async def read_non_active_users(_=Depends(auth_middleware.is_login)):
    users = try_catch_handler(lambda: User_Service.get_all_non_active_users())
    return response_service.get_success_response(data=users, message="users fetched successfully")

# ------------------------------- Users Operations ---------------------------------


@router.post("/login")
async def login_user(UserLogin: VLoginUser):
    data: dict = try_catch_handler(lambda: User_Service.user_login(UserLogin))
    user: dict = data["data"]
    message = data["message"]
    code = data["code"]

    if user is None:
        return response_service.get_error_response(data=None, message=message, status_code=code)

    response = set_tokens(user=user, message=message)
    return response


@router.post("/register")
async def register_user(UserRegister: VRegisterUser):
    data: dict = try_catch_handler(
        lambda: User_Service.register_user(UserRegister))
    user = data["data"]
    message = data["message"]
    code = data["code"]
    if user is None:
        return response_service.get_error_response(message=message, status_code=code)

    response = await set_tokens(user=user, message=message)
    return response


@router.post("/logout")
async def log_out(request: Request, response: Response, _=Depends(auth_middleware.is_login)):
    keys = [Constants.token, Constants.refresh_token]
    return response_service.delete_response_cookies(
        response=response,
        keys=keys,
        message="Logged out successfully"
    )

# --------------------------------------------------------------------------

#  ------------------------------ Helper Functions -------------------------


def set_tokens(user, message) -> Response:
    response: Response = response_service.return_response(
        data=user, message=message, status_code=200)
    # Create Tokens :
    token = try_catch_handler(
        lambda: Jwt.create_token({"user_id": str(user["id"])}, date_time_handler.return_current_date_time_with_hours(1)))
    refresh_token = try_catch_handler(
        lambda: Jwt.create_token({"user_id": str(user["id"])}, date_time_handler.return_current_date_time_with_days(5)))
    # Add tokens to response :
    try_catch_handler(lambda: response_service.update_response_with_cookies(
        response=response, value=token, key=Constants.token))
    try_catch_handler(lambda: response_service.update_response_with_cookies(
        response=response, value=refresh_token, key=Constants.refresh_token))
    return response
