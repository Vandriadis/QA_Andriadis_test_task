from typing import TypeVar, Type
from pydantic import ValidationError
from src.http.response import ResponseContext
from src.config.settings import settings

T = TypeVar("T")


def parse_json_as(model_class: Type[T], response: ResponseContext) -> T:
    content_type = response.headers.get("Content-Type", "").lower()
    if "application/json" not in content_type and response.status_code != 204:
        raise ContractViolationError(
            f"Expected JSON Content-Type, got: {content_type}",
            response=response
        )

    try:
        data = response.json()
    except ValueError as e:
        raise ContractViolationError(
            f"Failed to parse response as JSON: {e}",
            response=response
        ) from e

    try:
        return model_class.model_validate(data)
    except ValidationError as e:
        body_preview = response.text[:settings.max_body_length]
        if len(response.text) > settings.max_body_length:
            body_preview += "... (truncated)"

        error_msg = (
            f"Contract violation: {model_class.__name__} validation failed\n"
            f"  URL: {response.method} {response.url}\n"
            f"  Status: {response.status_code}\n"
            f"  Response body: {body_preview}\n"
            f"  Validation errors: {e.errors()}"
        )
        raise ContractViolationError(error_msg, response=response) from e


class ContractViolationError(Exception):
    def __init__(self, message: str, response: ResponseContext):
        super().__init__(message)
        self.response = response

