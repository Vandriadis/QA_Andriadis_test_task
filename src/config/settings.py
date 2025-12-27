from dataclasses import dataclass


@dataclass
class Settings:
    base_url: str = "https://petstore.swagger.io/v2"
    timeout: int = 10
    max_body_length: int = 1000


settings = Settings()

