from pydantic import BaseModel, ConfigDict


class BaseStrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

