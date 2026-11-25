from pymongo import MongoClient
from pymongo.collection import Collection

from app.core.config import settings

client = MongoClient(settings.mongodb_url)
db = client[settings.mongodb_db]


def get_products_collection() -> Collection:
    """FastAPI dependency that gives routes access to the products collection."""
    return db["products"]