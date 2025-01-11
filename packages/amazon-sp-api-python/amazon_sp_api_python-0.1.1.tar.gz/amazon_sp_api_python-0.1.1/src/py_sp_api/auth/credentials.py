from typing import Literal


class SPAPIConfig:
    def __init__(
        self,
        client_id,
        client_secret,
        refresh_token=None,
        region="NA",
        access_token=None,
        scope=None,
        grant_type: Literal["refresh_token", "client_credentials"] = "refresh_token",
    ):
        """
        SPAPIConfig is a configuration object for the SP-API client.
        :param client_id: The client ID for the SP-API client.
        :param client_secret: The client secret for the SP-API client.
        :param refresh_token: The refresh token for the SP-API client.
        :param region: The region for the SP-API client. (default: "NA" for North America)
        :param access_token: Access token for SP-API client. Initially empty, filled by LWA request. (default: None)
        :param scope: The scope for the SP-API client. Required for "client_credentials" grant type. (default: None)
        :param grant_type: Grant type for client ["refresh_token"|"client_credentials"]. (default: "refresh_token")
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.region = region
        self.scope = scope
        self.access_token = access_token  # Initially empty, filled by LWA request method
        self.grant_type = grant_type

        if grant_type == "client_credentials" and not scope:
            raise ValueError("Scope must be provided for grant_type 'client_credentials'")
