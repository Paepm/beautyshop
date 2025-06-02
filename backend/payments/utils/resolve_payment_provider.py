class ResolvePaymentProvider:
    """
    A utility class to resolve the payment provider based on the payment method.
    """

    def resolve_payment_provider(method: str) -> str:
        """
        Maps a payment_method (e.g. 'klarna') to its provider (e.g. 'stripe').

        Args:
            method (str): The payment method selected by the user.

        Returns:
            str: The corresponding payment provider.

        Raises:
            ValueError: If the method is not supported.
        """
        stripe_methods = {"card", "sofort", "bancontact", "sepa_debit", "klarna"}

        if method in stripe_methods:
            return "stripe"
        elif method == "paypal":
            return "paypal"

        raise ValueError(f"Unsupported payment method: {method}")
