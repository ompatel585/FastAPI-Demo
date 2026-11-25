"""Database logic for products. Routes call these functions; they never talk to MongoDB directly."""

from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.collection import Collection

from app.schemas.product import ProductCreate, ProductUpdate


def _to_dict(doc: dict) -> dict:
    """Convert a MongoDB document to a plain dict (ObjectId `_id` -> string `id`)."""
    doc["id"] = str(doc.pop("_id"))
    return doc


def _object_id(product_id: str) -> ObjectId | None:
    return ObjectId(product_id) if ObjectId.is_valid(product_id) else None


def list_products(collection: Collection) -> list[dict]:
    return [_to_dict(doc) for doc in collection.find()]


def get_product(collection: Collection, product_id: str) -> dict | None:
    oid = _object_id(product_id)
    if oid is None:
        return None
    doc = collection.find_one({"_id": oid})
    return _to_dict(doc) if doc else None


def create_product(collection: Collection, data: ProductCreate) -> dict:
    doc = data.model_dump()
    result = collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return _to_dict(doc)


def update_product(collection: Collection, product_id: str, data: ProductUpdate) -> dict | None:
    oid = _object_id(product_id)
    if oid is None:
        return None
    changes = data.model_dump(exclude_unset=True)  # only the fields the client sent
    if not changes:
        return get_product(collection, product_id)
    doc = collection.find_one_and_update(
        {"_id": oid},
        {"$set": changes},
        return_document=ReturnDocument.AFTER,
    )
    return _to_dict(doc) if doc else None


def delete_product(collection: Collection, product_id: str) -> bool:
    oid = _object_id(product_id)
    if oid is None:
        return False
    return collection.delete_one({"_id": oid}).deleted_count == 1