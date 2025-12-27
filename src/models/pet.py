from typing import Literal, Optional
from src.models.base import BaseStrictModel


class Category(BaseStrictModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Tag(BaseStrictModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Pet(BaseStrictModel):
    id: int
    category: Optional[Category] = None
    name: str
    photoUrls: list[str]
    tags: Optional[list[Tag]] = None
    status: Optional[Literal["available", "pending", "sold"]] = None

