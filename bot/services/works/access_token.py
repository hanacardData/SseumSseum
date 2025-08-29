import time
from logging import Logger

import jwt
import requests
from cryptography.hazmat.primitives import serialization

from bot.config.settings import settings
from bot.logger import logger


class TokenManager:
    def __init__(self, logger: Logger):
        self._access_token = None
        self._token_expiry = 0
        self.logger = logger

    def get_token(self) -> str:
        """get access token."""
        if self._access_token and not self.__is_token_expired:
            self.logger.debug("Returning cached access token.")
            return self._access_token

        self.logger.debug("Token expired or not available, requesting new token.")
        return self._request_new_token()

    def _request_new_token(self) -> str:
        """request new access token when expired."""
        now = int(time.time())
        exp = now + 3600
        payload = {
            "iss": settings.works_client_id,
            "sub": settings.service_account,
            "iat": now,
            "exp": exp,
        }
        try:
            with open(settings.private_key_path, "r") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read().encode(), password=None
                )
            encoded_jwt = jwt.encode(payload, private_key, algorithm="RS256")
        except Exception as e:
            self.logger.error(f"Error loading private key: {e}")
            raise

        token_url = "https://auth.worksmobile.com/oauth2/v2.0/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        data = {
            "assertion": encoded_jwt,
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "client_id": settings.works_client_id,
            "client_secret": settings.works_client_secret,
            "scope": "bot bot.message bot.read",
        }

        try:
            response = requests.post(token_url, headers=headers, data=data)
            response.raise_for_status()
        except requests.RequestException as e:
            self.logger.error(f"Token request failed: {e}")
            raise

        if response.status_code == 200:
            token_data = response.json()
            self._access_token = token_data["access_token"]
            self._token_expiry = exp
            return self._access_token
        else:
            self.logger.error(
                f"Failed to get token, status code: {response.status_code}"
            )
            self.logger.error(f"Response: {response.text}")
            raise Exception("Token request failed")

    @property
    def __is_token_expired(self) -> bool:
        return int(time.time()) >= self._token_expiry - 60


token_manager = TokenManager(logger)


def set_headers() -> dict[str, str]:
    token = token_manager.get_token()
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
