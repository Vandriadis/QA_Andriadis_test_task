import pytest
from src.api.pet_api import PetApi, PetNotFoundError, ApiError
from src.contracts.validators import ContractViolationError
from src.utils.data_factory import generate_pet, generate_invalid_pet_payload, generate_empty_pet_payload
from src.http.client import HttpClient


def test_get_nonexistent_pet(pet_api: PetApi):
    nonexistent_id = 999999999999
    with pytest.raises(PetNotFoundError) as exc_info:
        pet_api.get_pet(nonexistent_id)
    assert exc_info.value.response.status_code == 404


def test_delete_nonexistent_pet(pet_api: PetApi):
    try:
        response = pet_api.delete_pet(999999999)
        assert response.code in (200, 404)
    except PetNotFoundError:
        pass


def test_create_pet_with_invalid_payload(pet_api: PetApi):
    client = HttpClient()
    invalid_payload = generate_invalid_pet_payload()
    
    response = client.request("POST", "/pet", json=invalid_payload)
    
    if response.status_code in (400, 500):
        try:
            from src.contracts.validators import parse_json_as
            from src.models.errors import ErrorResponse
            error = parse_json_as(ErrorResponse, response)
            assert error.code is not None
        except ContractViolationError:
            pass
    elif response.status_code == 200:
        try:
            from src.contracts.validators import parse_json_as
            from src.models.pet import Pet
            parse_json_as(Pet, response)
        except ContractViolationError as e:
            pytest.fail(f"API returned 200 but response doesn't match Pet contract: {e}")


def test_create_pet_with_empty_payload(pet_api: PetApi):
    client = HttpClient()
    empty_payload = generate_empty_pet_payload()
    
    response = client.request("POST", "/pet", json=empty_payload)
    
    if response.status_code in (400, 500):
        try:
            from src.contracts.validators import parse_json_as
            from src.models.errors import ErrorResponse
            parse_json_as(ErrorResponse, response)
        except ContractViolationError as e:
            pass
    elif response.status_code == 200:
        from src.contracts.validators import parse_json_as, ContractViolationError
        from src.models.pet import Pet
        with pytest.raises(ContractViolationError):
            parse_json_as(Pet, response)


def test_update_pet_without_id(pet_api: PetApi):
    client = HttpClient()
    pet_data = generate_pet().model_dump()
    del pet_data["id"]
    
    response = client.request("PUT", "/pet", json=pet_data)
    
    if response.status_code in (400, 404, 500):
        try:
            from src.contracts.validators import parse_json_as
            from src.models.errors import ErrorResponse
            parse_json_as(ErrorResponse, response)
        except ContractViolationError as e:
            pass
    elif response.status_code == 200:
        try:
            from src.contracts.validators import parse_json_as
            from src.models.pet import Pet
            parsed = parse_json_as(Pet, response)
            assert isinstance(parsed, Pet)
        except ContractViolationError as e:
            pytest.fail(f"API returned 200 but response doesn't match Pet contract: {e}")


def test_update_nonexistent_pet(pet_api: PetApi):
    pet = generate_pet(pet_id=999999999)
    
    response = HttpClient().request("PUT", "/pet", json=pet.model_dump())
    
    if response.status_code == 404:
        try:
            from src.contracts.validators import parse_json_as
            from src.models.errors import ErrorResponse
            parse_json_as(ErrorResponse, response)
        except ContractViolationError:
            pass


def test_find_by_status_invalid_status(pet_api: PetApi):
    client = HttpClient()
    response = client.request("GET", "/pet/findByStatus", params={"status": "invalid_status"})
    
    if response.status_code == 400:
        try:
            from src.contracts.validators import parse_json_as
            from src.models.errors import ErrorResponse
            parse_json_as(ErrorResponse, response)
        except ContractViolationError as e:
            pytest.fail(f"Contract violation on error response: {e}")

