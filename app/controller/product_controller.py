from fastapi import APIRouter, Depends
from service.product_service import Product_service, VCreateProduct, VUpdateProduct
from service.response_service import response_service
from utils.try_catch_handler import try_catch_handler
from utils.Cloudinary_handler import Cloudinary_handler
from middleware.auth_middleware import auth_middleware
from pydantic import BaseModel
router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"message": "Not found"}},
)

# ------------------------------- Product Operations ---------------------------------
message = "Product updated successfully"

# Admins :


class VImage(BaseModel):
    image_url: str


@router.post("/image")
async def get_image(product: VImage):
    return await try_catch_handler(lambda: Cloudinary_handler.delete_image(product.image_url))


@router.post("/add-new-product")
async def add_new_product(product: VCreateProduct = Depends(), _=Depends(auth_middleware.is_admin)):
    product.image = await try_catch_handler(lambda: Cloudinary_handler.upload_image(product.image))
    if not product.image:
        return response_service.get_error_response(data=None, message="Failed in uploading image", status_code=400)
    result = try_catch_handler(
        lambda: Product_service.add_new_product(product))
    if not result:
        return response_service.get_error_response(data=None, message="Failed in adding new product", status_code=400)
    return response_service.get_success_response(data=result, message=message)


@router.patch("/update-product/{product_id}")
async def update_product(product_id: int, product: VUpdateProduct, _=Depends(auth_middleware.is_admin)):
    result = try_catch_handler(
        lambda: Product_service.update_product(product_id, product))
    if not result:
        return response_service.get_error_response(data=None, message="Failed in updating product", status_code=400)
    return response_service.get_success_response(data=result, message=message)


@router.delete("/delete-product/{product_id}")
async def delete_product(product_id: int, _=Depends(auth_middleware.is_admin)):
    result = await try_catch_handler(
        lambda:  Product_service.delete_product(product_id))

    product = result["data"]
    message = result["message"]
    code = result["code"]
    return response_service.return_response(data=product, message=message, status_code=code)

# All :


@router.get("/all")
async def read_all_products():
    results = try_catch_handler(lambda: Product_service.get_all_products())
    return response_service.get_success_response(data=results, message=message)


@router.get("/{product_id}")
async def read_product(product_id: int):
    result = try_catch_handler(
        lambda: Product_service.get_product_by_id(product_id))
    return response_service.get_success_response(data=result, message=message)
