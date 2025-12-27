import pytest
from src.api.pet_api import PetApi
from src.contracts.validators import parse_json_as, ContractViolationError
from src.models.pet import Pet
from src.models.api_response import ApiResponse
from src.utils.data_factory import generate_pet
from src.http.client import HttpClient


def test_get_pet_contract_compliance(pet_api: PetApi):
    pet = generate_pet()
    created = pet_api.create_pet(pet)
    
    try:
        response = HttpClient().request("GET", f"/pet/{created.id}")
        assert response.status_code == 200
        
        parsed = parse_json_as(Pet, response)
        assert isinstance(parsed, Pet)
        assert parsed.id == created.id
    finally:
        pet_api.delete_pet(created.id)


def test_create_pet_contract_compliance(pet_api: PetApi):
    pet = generate_pet()
    
    response = HttpClient().request("POST", "/pet", json=pet.model_dump())
    assert response.status_code == 200
    
    parsed = parse_json_as(Pet, response)
    assert isinstance(parsed, Pet)
    assert parsed.id == pet.id
    
    pet_api.delete_pet(parsed.id)


def test_update_pet_contract_compliance(pet_api: PetApi):
    pet = generate_pet()
    created = pet_api.create_pet(pet)
    
    try:
        updated_pet = generate_pet(pet_id=created.id, name="Updated")
        response = HttpClient().request("PUT", "/pet", json=updated_pet.model_dump())
        assert response.status_code == 200
        
        parsed = parse_json_as(Pet, response)
        assert isinstance(parsed, Pet)
        assert parsed.id == created.id
    finally:
        pet_api.delete_pet(created.id)


def test_delete_pet_contract_compliance(pet_api: PetApi):
    pet = generate_pet()
    created = pet_api.create_pet(pet)
    
    response = HttpClient().request("DELETE", f"/pet/{created.id}")
    assert response.status_code == 200
    
    parsed = parse_json_as(ApiResponse, response)
    assert isinstance(parsed, ApiResponse)
    assert parsed.code == 200


def test_find_by_status_contract_compliance(pet_api: PetApi):
    pet = generate_pet(status="available")
    created = pet_api.create_pet(pet)
    
    try:
        response = HttpClient().request("GET", "/pet/findByStatus", params={"status": "available"})
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        
        for item in data[:5]:
            parsed = Pet.model_validate(item)
            assert isinstance(parsed, Pet)
    finally:
        pet_api.delete_pet(created.id)


def test_pet_model_strictness():
    pet_data = {
        "id": 1,
        "name": "Test",
        "photoUrls": ["url1"],
        "extra_field": "should_fail"
    }
    
    with pytest.raises(Exception):
        Pet.model_validate(pet_data)

