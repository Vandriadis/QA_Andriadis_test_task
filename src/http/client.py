from typing import Optional
import requests
from src.config.settings import settings
from src.http.response import ResponseContext


class HttpClient:
    def __init__(self, base_url: str = None, timeout: int = None):
        self.base_url = base_url or settings.base_url
        self.timeout = timeout or settings.timeout

    def request(
        self,
        method: str,
        path: str,
        json: Optional[dict] = None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        **kwargs
    ) -> ResponseContext:
        url = f"{self.base_url}{path}"
        default_headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if headers:
            default_headers.update(headers)

        response = requests.request(
            method=method.upper(),
            url=url,
            json=json,
            params=params,
            headers=default_headers,
            timeout=self.timeout,
            **kwargs
        )

        return ResponseContext(
            method=method.upper(),
            url=url,
            status_code=response.status_code,
            headers=dict(response.headers),
            text=response.text,
            elapsed=response.elapsed.total_seconds()
        )

