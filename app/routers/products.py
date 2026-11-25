"""HTTP layer for products: request/response handling only, no database code."""

from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.collection import Collection

from app.db.mongodb import get_products_collection
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])

NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")


@router.get("", response_model=list[ProductOut])
def list_products(collection: Collection = Depends(get_products_collection)):
    return product_service.list_products(collection)


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: str, collection: Collection = Depends(get_products_collection)):
    product = product_service.get_product(collection, product_id)
    if product is None:
        raise NOT_FOUND
    return product


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, collection: Collection = Depends(get_products_collection)):
    return product_service.create_product(collection, data)


@router.patch("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: str,
    data: ProductUpdate,
    collection: Collection = Depends(get_products_collection),
):
    product = product_service.update_product(collection, product_id, data)
    if product is None:
        raise NOT_FOUND
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str, collection: Collection = Depends(get_products_collection)):
    if not product_service.delete_product(collection, product_id):
        raise NOT_FOUND