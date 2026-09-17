import json
import urllib3
import requests
from .authentication import WazuhAuthenticator

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WazuhClient:

    def __init__(self, base_url, username, password, verify_ssl=False, port=None):
        self.base_url   = base_url.rstrip("/")
        self.verify_ssl = verify_ssl
        self.port       = port

        # Authenticate and get JWT — exactly as Wazuh docs show
        auth  = WazuhAuthenticator(base_url, username, password, verify_ssl, port)
        token = auth.login()

        # All subsequent requests use this header
        self.requests_headers = {
            "Content-Type":  "application/json",
            "Authorization": f"Bearer {token}",
        }

    def get(self, endpoint, **kwargs):
        url      = f"{self.base_url}:{self.port}{endpoint}"
        response = requests.get(
            url,
            headers = self.requests_headers,
            verify  = self.verify_ssl,
            **kwargs,
        )
        return json.loads(response.content.decode())

    def post(self, endpoint, **kwargs):
        url      = f"{self.base_url}:{self.port}{endpoint}"
        response = requests.post(
            url,
            headers = self.requests_headers,
            verify  = self.verify_ssl,
            **kwargs,
        )
        return json.loads(response.content.decode())

    def put(self, endpoint, **kwargs):
        url      = f"{self.base_url}:{self.port}{endpoint}"
        response = requests.put(
            url,
            headers = self.requests_headers,
            verify  = self.verify_ssl,
            **kwargs,
        )
        return json.loads(response.content.decode())

    def delete(self, endpoint, **kwargs):
        url      = f"{self.base_url}:{self.port}{endpoint}"
        response = requests.delete(
            url,
            headers = self.requests_headers,
            verify  = self.verify_ssl,
            **kwargs,
        )
        return json.loads(response.content.decode())


def get_platform_wazuh_client():
    from intergration.models import PlatformIntegration

    integration = PlatformIntegration.objects.get(
        integration_type = "wazuh",
        enabled          = True,
    )
    cred = integration.credential

    return WazuhClient(
        base_url   = integration.base_url,
        username   = cred.username,
        password   = cred.password,
        verify_ssl = integration.verify_ssl,
        port      = integration.port,
    )