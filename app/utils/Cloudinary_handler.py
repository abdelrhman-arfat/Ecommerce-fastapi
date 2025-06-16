import os
import cloudinary
import os
from cloudinary.uploader import upload
from fastapi import UploadFile
from fastapi import UploadFile
from utils.custom_http_exception import custom_http_exception
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)


class Cloudinary_handler:
    async def upload_image(image: UploadFile):
        try:
            upload_result = upload(
                image.file, public_id=datetime.now().strftime("%Y%m%d%H%M%S"), overwrite=True
            )
            file_url = upload_result['secure_url']
            return file_url
        except Exception as e:
            raise custom_http_exception(
                data=None, message=str(e), status_code=400)

    async def delete_image(image_url: str):
        try:
            path = image_url.split("/upload/")[-1]
            public_id = "/".join(path.split("/")[1:])
            public_id = public_id.split(".")[0]
            print(public_id)
            result = cloudinary.uploader.destroy(public_id)
            return result
        except Exception as e:
            raise custom_http_exception(
                data=None, message=str(e), status_code=400)
