from abc import ABC, abstractmethod


class BasePaymentProvider(ABC):
    """
    Abstract base class that all payment providers must implement.
    """

    def __init__(self, user):
        self.user = user

    @abstractmethod
    def create_payment_intent(self, amount: float, currency: str = "eur") -> dict:
        """
        Creates a payment intent and returns metadata like client_secret.

        Args:
            amount (float): The total amount to charge.
            currency (str): Currency code, default is EUR.

        Returns:
            dict: A dictionary with provider-specific response data.
        """
        pass

    @abstractmethod
    def confirm_payment(self, payment_intent_id: str) -> bool:
        """
        Confirms the payment with the given intent ID.

        Returns:
            bool: True if payment is confirmed, False otherwise.
        """
        pass

    @abstractmethod
    def cancel_payment(self, payment_intent_id: str) -> bool:
        """
        Cancels the payment with the given intent ID.

        Returns:
            bool: True if successfully cancelled, False otherwise.
        """
        pass
