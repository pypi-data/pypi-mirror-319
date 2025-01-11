"""Base SPAPIClient gets copied to each generated client."""

from typing import Optional, Dict, Any
from .api_client import ApiClient  # type: ignore will be relative imports when copied into each generated client
from .configuration import Configuration  # type: ignore will be relative imports when copied into each generated client
from py_sp_api.auth.credentials import SPAPIConfig
from py_sp_api.auth.LwaRequest import AccessTokenCache


class SPAPIClient(ApiClient):
    def __init__(self, spapi_config: SPAPIConfig, config: Configuration = None):
        config = config or Configuration()
        super().__init__(configuration=config)
        self.spapi_config = spapi_config
        self.access_token_cache = AccessTokenCache()

    def call_api(
        self,
        method: str,
        url: str,
        header_params: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[Dict[str, Any]] = None,
        _request_timeout: Optional[int] = None,
    ):
        header_params = header_params or {}
        header_params["x-amz-access-token"] = self.access_token_cache.get_lwa_access_token(
            client_id=self.spapi_config.client_id,
            client_secret=self.spapi_config.client_secret,
            refresh_token=self.spapi_config.refresh_token,
            grant_type=self.spapi_config.grant_type,
            scope=self.spapi_config.scope,
        )
        return super().call_api(method, url, header_params, body, post_params, _request_timeout)
