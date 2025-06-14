from fastapi import HTTPException

""" 
    When use this func return it like this:
        try_catch_handler(lambda: your_function(your_args))
        but not like this:
        try_catch_handler(your_function(your_args))
        because this will make the function work before your wrapper
"""


def try_catch_handler(func):
    try:
        return func()
    except Exception as e:
        print("error ❌‼️ -->", e)
        raise HTTPException(status_code=400, detail=str(e))
