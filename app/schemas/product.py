from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    quantity: int = Field(default=0, ge=0)


class ProductCreate(ProductBase):
    """Body for POST /products."""


class ProductUpdate(BaseModel):
    """Body for PATCH /products/{id}. Every field is optional."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    price: float | None = Field(default=None, gt=0)
    quantity: int | None = Field(default=None, ge=0)


class ProductOut(ProductBase):
    """What the API returns."""

    id: str