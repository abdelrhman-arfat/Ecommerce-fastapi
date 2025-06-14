from fastapi import FastAPI, Request
from controller.user_controller import router as user_router

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

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
