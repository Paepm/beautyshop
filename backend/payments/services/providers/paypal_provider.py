import requests
from decouple import config

from payments.services.providers.base import BasePaymentProvider


class PayPalProvider(BasePaymentProvider):
    def __init__(self, user, oder=None):
        super().__init__(user)
        self.order = oder
        self.client_id = config("PAYPAL_CLIENT_ID")
        self.client_secret = config("PAYPAL_CLIENT_SECRET")
        self.base_url = "https://api-m.sandbox.paypal.com"  # Use sandbox for testing
        self.access_token = self._get_access_token()

    def _get_access_token(self) -> str:
        """
        Obtain an access token from PayPal using client credentials.

        Returns:
            str: The access token to authenticate API requests.
        """
        url = f"{self.base_url}/v1/oauth2/token"
        response = requests.post(
            url,
            auth=(self.client_id, self.client_secret),
            data={"grant_type": "client_credentials"},
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def create_checkout_session(self, success_url: str, cancel_url: str) -> dict:
        """
        Create a PayPal Checkout session (Order) and return the redirect link.

        Args:
            success_url (str): URL to redirect after successful payment.
            cancel_url (str): URL to redirect if user cancels.

        Returns:
            str: The PayPal approval URL to redirect the user.
        """
        if not self.order:
            raise ValueError("Order is not set. Please provide an order.")

        url = f"{self.base_url}/v2/checkout/orders"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        data = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "EUR",
                        "value": str(self.order.total_price),
                    },
                    "custom_id": str(self.order.id),  # Custom ID to link order
                },
            ],
            "application_context": {
                "return_url": success_url,
                "cancel_url": cancel_url,
            },
        }

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        links = response.json().get("links", [])

        for link in links:
            if link["rel"] == "approve":
                return link["href"]

        raise Exception("No Approval link found in Paypal response.")

    def create_payment_intent(self, amount: float, currency: str = "eur") -> dict:
        raise NotImplementedError("This provider uses checkout session instead.")

    def confirm_payment(self, payment_intent_id: str) -> bool:
        """
        Confirms the payment with the given intent ID.

        Returns:
            bool: True if payment is confirmed, False otherwise.
        """
        return True

    def cancel_payment(self, payment_intent_id: str) -> bool:
        """
        Cancels the payment with the given intent ID.

        Returns:
            bool: True if successfully cancelled, False otherwise.
        """
        return False
