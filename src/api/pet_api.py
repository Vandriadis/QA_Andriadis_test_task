from typing import List
from pydantic import ValidationError
from src.http.client import HttpClient
from src.http.response import ResponseContext
from src.contracts.validators import parse_json_as, ContractViolationError
from src.models.pet import Pet
from src.models.api_response import ApiResponse
from src.models.errors import ErrorResponse


class PetApi:
    def __init__(self, client: HttpClient = None):
        self.client = client or HttpClient()

    def create_pet(self, pet: Pet) -> Pet:
        response = self.client.request("POST", "/pet", json=pet.model_dump())
        if response.status_code != 200:
            self._handle_error_response(response)
        return parse_json_as(Pet, response)

    def get_pet(self, pet_id: int) -> Pet:
        response = self.client.request("GET", f"/pet/{pet_id}")
        if response.status_code == 404:
            raise PetNotFoundError(f"Pet with id {pet_id} not found", response)
        if response.status_code != 200:
            self._handle_error_response(response)
        return parse_json_as(Pet, response)

    def update_pet(self, pet: Pet) -> Pet:
        response = self.client.request("PUT", "/pet", json=pet.model_dump())
        if response.status_code != 200:
            self._handle_error_response(response)
        return parse_json_as(Pet, response)

    def delete_pet(self, pet_id: int) -> ApiResponse:
        response = self.client.request("DELETE", f"/pet/{pet_id}")
        if response.status_code not in (200, 404):
            self._handle_error_response(response)
        if response.status_code == 404:
            try:
                return parse_json_as(ApiResponse, response)
            except ContractViolationError:
                raise PetNotFoundError(f"Pet with id {pet_id} not found", response)
        return parse_json_as(ApiResponse, response)

    def find_by_status(self, status: str) -> List[Pet]:
        response = self.client.request("GET", "/pet/findByStatus", params={"status": status})
        if response.status_code != 200:
            self._handle_error_response(response)
        data = response.json()
        if not isinstance(data, list):
            raise ContractViolationError(
                f"Expected list of pets, got: {type(data)}",
                response=response
            )
        try:
            return [Pet.model_validate(item) for item in data]
        except ValidationError as e:
            raise ContractViolationError(
                f"Contract violation: One or more pets in list failed validation: {e.errors()}",
                response=response
            ) from e

    def _handle_error_response(self, response: ResponseContext):
        try:
            error = parse_json_as(ErrorResponse, response)
            raise ApiError(
                f"API error: {error.message or 'Unknown error'} (code: {error.code})",
                response=response,
                error_response=error
            )
        except ContractViolationError:
            raise ApiError(
                f"Unexpected API response: {response.status_code}",
                response=response
            )


class PetNotFoundError(Exception):
    def __init__(self, message: str, response: ResponseContext):
        super().__init__(message)
        self.response = response


class ApiError(Exception):
    def __init__(self, message: str, response: ResponseContext, error_response=None):
        super().__init__(message)
        self.response = response
        self.error_response = error_response

