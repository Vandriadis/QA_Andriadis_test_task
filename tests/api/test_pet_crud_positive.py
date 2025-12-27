import pytest
from src.api.pet_api import PetApi, PetNotFoundError
from src.utils.data_factory import generate_pet


def test_create_get_update_delete_flow(pet_api: PetApi):
    pet = generate_pet()
    
    created = pet_api.create_pet(pet)
    assert created.id == pet.id
    assert created.name == pet.name
    assert created.status == pet.status
    
    retrieved = pet_api.get_pet(pet.id)
    assert retrieved.id == pet.id
    assert retrieved.name == pet.name
    
    updated_pet = generate_pet(pet_id=pet.id, name="UpdatedName", status="sold")
    updated = pet_api.update_pet(updated_pet)
    assert updated.id == pet.id
    assert updated.name == "UpdatedName"
    assert updated.status == "sold"
    
    delete_response = pet_api.delete_pet(pet.id)
    assert delete_response.code == 200
    
    with pytest.raises(PetNotFoundError):
        pet_api.get_pet(pet.id)


def test_create_pet_with_all_fields(pet_api: PetApi):
    from src.models.pet import Category, Tag
    
    category = Category(id=1, name="Dogs")
    tags = [Tag(id=1, name="friendly"), Tag(id=2, name="cute")]
    pet = generate_pet(
        name="FullPet",
        status="available",
        category=category,
        tags=tags
    )
    
    created = pet_api.create_pet(pet)
    assert created.category is not None
    assert created.category.name == "Dogs"
    assert created.tags is not None
    assert len(created.tags) == 2


def test_find_by_status(pet_api: PetApi):
    pet = generate_pet(status="available")
    created = pet_api.create_pet(pet)
    
    try:
        pets = pet_api.find_by_status("available")
        assert len(pets) > 0
        assert any(p.id == created.id for p in pets)
    finally:
        pet_api.delete_pet(created.id)

