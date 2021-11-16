import sys
from os import getenv
from typing import Any
from typing import Dict
from typing import List

from dotenv import load_dotenv  # type: ignore[import]
from paypalcheckoutsdk.core import PayPalHttpClient  # type: ignore[import]
from paypalcheckoutsdk.core import SandboxEnvironment

from app.core.config import settings

load_dotenv()

CLIENT_ID = getenv("PAYPAL-SANDBOX-CLIENT-ID")
CLIENT_SECRET = getenv("PAYPAL-SANDBOX-CLIENT-SECRET")
LIVE_CLIENT_ID = getenv("PAYPAL-LIVE-CLIENT-ID")
LIVE_CLIENT_SECRET = getenv("PAYPAL-LIVE-CLIENT-SECRET")

# https://developer.paypal.com/docs/checkout/reference/server-integration/setup-sdk/
class PayPalClient:
    def __init__(self) -> None:
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.live_client_id = LIVE_CLIENT_ID
        self.live_client_secret = LIVE_CLIENT_SECRET

        """Set up and return PayPal Python SDK environment with PayPal access credentials.
		   This sample uses SandboxEnvironment. In production, use LiveEnvironment."""

        if settings.ENVIRONMENT == "PROD":
            self.environment = LiveEnvironment(
                client_id=self.live_client_id, client_secret=self.live_client_secret
            )
        else:
            self.environment = SandboxEnvironment(
                client_id=self.client_id, client_secret=self.client_secret
            )

        """ Returns PayPal HTTP client instance with environment that has access
			credentials context. Use this instance to invoke PayPal APIs, provided the
			credentials have access. """
        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data: str) -> Dict[str, Any]:
        """
        Function to print all json data in an organized readable manner
        """
        result = {}
        if sys.version_info[0] < 3:
            itr = json_data.__dict__.iteritems()
        else:
            itr = json_data.__dict__.items()
        for key, value in itr:
            # Skip internal attributes.
            if key.startswith("__"):
                continue
            result[key] = (
                self.array_to_json_array(value)
                if isinstance(value, list)
                else self.object_to_json(value)
                if not self.is_primittive(value)
                else value
            )
        return result

    def array_to_json_array(self, json_array: List[Any]) -> List[str]:
        result: List[str] = []
        if isinstance(json_array, list):
            for item in json_array:
                result.append(
                    self.object_to_json(item)
                    if not self.is_primittive(item)
                    else self.array_to_json_array(item)
                    if isinstance(item, list)
                    else item
                )
        return result

    def is_primittive(self, data: str) -> bool:
        return isinstance(data, str) or isinstance(data, str) or isinstance(data, int)
