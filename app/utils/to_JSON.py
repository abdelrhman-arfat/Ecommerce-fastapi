from fastapi.encoders import jsonable_encoder


def to_JSON(data, exclude=None):
    return jsonable_encoder(data, exclude=exclude)
