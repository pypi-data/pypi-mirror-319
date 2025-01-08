from typing import NoReturn

import httpx

from mailtrap.exceptions import APIError
from mailtrap.exceptions import AuthorizationError
from mailtrap.mail.base import BaseMail


class MailtrapClient:
    DEFAULT_HOST = "send.api.mailtrap.io"
    DEFAULT_PORT = 443

    def __init__(
        self,
        token: str,
        api_host: str = DEFAULT_HOST,
        api_port: int = DEFAULT_PORT,
    ) -> None:
        self.token = token
        self.api_host = api_host
        self.api_port = api_port

    def send(self, mail: BaseMail) -> dict[str, bool | list[str]]:
        url = f"{self.base_url}/api/send"
        response = httpx.post(url, headers=self.headers, json=mail.api_data)

        if response.is_success:
            data: dict[str, bool | list[str]] = response.json()
            return data

        self._handle_failed_response(response)

    async def asend(self, mail: BaseMail) -> dict[str, bool | list[str]]:
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/api/send"
            response = await client.post(url, headers=self.headers, json=mail.api_data)

            if not response.is_success:
                self._handle_failed_response(response)

            data: dict[str, bool | list[str]] = response.json()
            return data

    @property
    def base_url(self) -> str:
        # flake8: noqa: E231
        return f"https://{self.api_host.rstrip('/')}:{self.api_port}"

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "User-Agent": (
                "mailtrap-python (https://github.com/railsware/mailtrap-python)"
            ),
        }

    @staticmethod
    def _handle_failed_response(response: httpx.Response) -> NoReturn:
        status_code = response.status_code
        data = response.json()

        if status_code == 401:
            raise AuthorizationError(data["errors"])

        raise APIError(status_code, data["errors"])
