from dataclasses import dataclass
from typing import Optional
import json


@dataclass
class ResponseContext:
    method: str
    url: str
    status_code: int
    headers: dict
    text: str
    elapsed: float

    def json(self) -> dict:
        try:
            return json.loads(self.text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {e}") from e

