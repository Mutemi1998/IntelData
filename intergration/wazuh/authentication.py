import json
import urllib3
import requests
from base64 import b64encode

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WazuhAuthenticator:

    def __init__(self, base_url, username, password, verify_ssl=False, port=5500):
        self.base_url   = base_url.rstrip("/")
        self.username   = username
        self.password   = password
        self.verify_ssl = verify_ssl
        self.port       = port

    def login(self):
        login_url  = f"{self.base_url}:{self.port}/security/user/authenticate"
        basic_auth = f"{self.username}:{self.password}".encode()

        login_headers = {
            "Content-Type":  "application/json",
            "Authorization": f"Basic {b64encode(basic_auth).decode()}",
        }

        try:
            print(f"[Wazuh] Attempting login to: {login_url}")

            response = requests.post(
                login_url,
                headers = login_headers,
                verify  = self.verify_ssl,
            )

            print(f"[Wazuh] Status code   : {response.status_code}")
            print(f"[Wazuh] Content-Type  : {response.headers.get('Content-Type')}")
            # print(f"[Wazuh] Raw response  : {response.content}")

        except requests.exceptions.ConnectionError as e:
            raise Exception(f"[Wazuh] Cannot connect to Wazuh — is the URL correct? {e}")

        except requests.exceptions.Timeout as e:
            raise Exception(f"[Wazuh] Connection timed out: {e}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"[Wazuh] Request failed: {e}")

        try:
            parsed = json.loads(response.content.decode())
            # print(f"[Wazuh] Parsed JSON: {parsed}")

        except json.JSONDecodeError as e:
            raise Exception(
                f"[Wazuh] Response is not valid JSON.\n"
                f"  Error        : {e}\n"
                f"  Status code  : {response.status_code}\n"
                f"  Raw content  : {response.content[:500]}"
            )

        try:
            token = parsed["data"]["token"]
            print(f"[Wazuh] Login successful. Token: {token[:30]}...")
            return token

        except KeyError as e:
            print(f"[Wazuh] Token not found in response. Missing key: {e}")
            print(f"[Wazuh] Full response: {parsed}")
            raise Exception(
                f"[Wazuh] Token not found in response.\n"
                f"  Missing key  : {e}\n"
                f"  Full response: {parsed}"
            )