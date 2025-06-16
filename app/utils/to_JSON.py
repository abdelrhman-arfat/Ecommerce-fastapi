from fastapi.encoders import jsonable_encoder


def to_JSON(data, exclude=None):
    return jsonable_encoder(data, exclude=exclude )

def return_code_data_message(message, data=None, code=400):
        return {
            "message": message,
            "data": data,
            "code": code
        }
