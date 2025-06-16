from fastapi import FastAPI, Request
from controller.user_controller import router as user_router
from controller.product_controller import router as product_router
from utils.custom_http_exception import custom_http_exception

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()
app.include_router(user_router)
app.include_router(product_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    wantedMessage = ""
    for err in errors:
        field = err["loc"][-1]
        msg = err["msg"]

        wantedMessage += f"{field}, " + msg

    if wantedMessage.endswith(", "):
        wantedMessage = wantedMessage[:-2] + " ; "

    return JSONResponse(
        status_code=422,
        content={
            "status": "fail",
            "message": "Validation error " + wantedMessage,
            "data": None
        },
    )


@app.exception_handler(custom_http_exception)
async def custom_exception_handler(request: Request, exc: custom_http_exception):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )
