from fastapi import APIRouter, HTTPException, status, Request
from models import Product
from auth_utils import require_auth
from bson import ObjectId
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=Product)
@require_auth
async def create_product(request: Request, product: Product, current_user: str):
    product.owner_id = current_user
    result = await router.app.mongodb["products"].insert_one(product.dict(by_alias=True))
    created_product = await router.app.mongodb["products"].find_one({"_id": result.inserted_id})
    return Product(**created_product)

@router.get("/", response_model=List[Product])
@require_auth
async def get_products(request: Request, current_user: str):
    products = await router.app.mongodb["products"].find({"owner_id": current_user}).to_list(1000)
    return [Product(**product) for product in products]

@router.get("/{product_id}", response_model=Product)
@require_auth
async def get_product(request: Request, product_id: str, current_user: str):
    product = await router.app.mongodb["products"].find_one({"_id": ObjectId(product_id), "owner_id": current_user})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**product)

@router.put("/{product_id}", response_model=Product)
@require_auth
async def update_product(request: Request, product_id: str, product_update: Product, current_user: str):
    product = await router.app.mongodb["products"].find_one({"_id": ObjectId(product_id), "owner_id": current_user})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()

    await router.app.mongodb["products"].update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_data}
    )

    updated_product = await router.app.mongodb["products"].find_one({"_id": ObjectId(product_id)})
    return Product(**updated_product)

@router.delete("/{product_id}")
@require_auth
async def delete_product(request: Request, product_id: str, current_user: str):
    result = await router.app.mongodb["products"].delete_one({"_id": ObjectId(product_id), "owner_id": current_user})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
