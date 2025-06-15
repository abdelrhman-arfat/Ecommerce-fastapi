from fastapi import FastAPI, Request
from controller.user_controller import router as user_router
from utils.custom_http_exception import custom_http_exception

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()
app.include_router(user_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    custom_errors = []

    for err in errors:
        custom_errors.append({
            "field": ".".join(map(str, err["loc"])),
            "message": err["msg"],
            "type": err["type"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "status": "fail",
            "message": "Validation error",
            "errors": custom_errors
        }
    )


@app.exception_handler(custom_http_exception)
async def custom_exception_handler(request: Request, exc: custom_http_exception):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )
