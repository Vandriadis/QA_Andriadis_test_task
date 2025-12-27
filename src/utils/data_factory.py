import random
from typing import Optional
from src.models.pet import Pet, Category, Tag


def generate_pet(
    pet_id: Optional[int] = None,
    name: Optional[str] = None,
    status: Optional[str] = None,
    photo_urls: Optional[list[str]] = None,
    category: Optional[Category] = None,
    tags: Optional[list[Tag]] = None
) -> Pet:
    if pet_id is None:
        pet_id = random.randint(1, 999999)
    if name is None:
        name = f"Pet_{random.randint(1000, 9999)}"
    if status is None:
        status = random.choice(["available", "pending", "sold"])
    if photo_urls is None:
        photo_urls = [f"https://example.com/photo_{i}.jpg" for i in range(random.randint(1, 3))]

    return Pet(
        id=pet_id,
        name=name,
        status=status,
        photoUrls=photo_urls,
        category=category,
        tags=tags
    )


def generate_invalid_pet_payload() -> dict:
    return {
        "invalid_field": "value",
        "id": "not_an_int",
        "name": 123,
        "photoUrls": "not_a_list"
    }


def generate_empty_pet_payload() -> dict:
    return {}


def generate_pet_without_required_fields() -> dict:
    return {
        "id": 123
    }

