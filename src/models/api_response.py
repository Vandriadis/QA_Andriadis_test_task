from typing import Optional
from src.models.base import BaseStrictModel


class ApiResponse(BaseStrictModel):
    code: Optional[int] = None
    type: Optional[str] = None
    message: Optional[str] = None

