from django.core import signing
from django.contrib.auth import login
from django.http import HttpRequest
from typing import Optional, Tuple

from accounts.forms import SignupForm
from accounts.models import CustomUser
from beautyshop.logging_config import setup_logger
from emails.services.email_confirmation import ConfirmationEmailService


class EmailConfirmationService:
    """
    Service for verifying a signed signup token, creating a new user, and sending a confirmation email.
    """

    def __init__(self, request: HttpRequest, token: str):
        """
        Initialize the service with the HTTP request and the signed token.

        Args:
            request (HttpRequest): The incoming request.
            token (str): The signed string containing user data.
            logger (Logger): Logger instance for logging errors and information.
        """
        self.request = request
        self.token = token
        self.logger = setup_logger(__name__)

    def verify_and_create_user(self) -> Tuple[Optional[CustomUser], Optional[str]]:
        """
        Verifies the signed token, validates the data, creates a new user, logs them in,
        and sends a confirmation email.

        Returns:
            Tuple[Optional[CustomUser], Optional[str]]: A tuple where the first element is the created user
            (or None if creation failed), and the second element is an error message (or None if successful).
        """
        try:
            user_data = signing.loads(
                self.token, max_age=60 * 60 * 24
            )  # max age of token is 60sec*60min*24h = 24 hours
            form = SignupForm(user_data)

            if form.is_valid():
                user = form.save()
                login(self.request, user)
                ConfirmationEmailService.send_confirmation_email(user)
                self.logger.info(
                    "Confirmation email successfully sent to %s", user.email
                )
                return user, None

            # Log for invalid form (valid token but invalid data)
            self.logger.warning(
                "Token is valid but SignupForm is invalid. Errors: %s | Data: %s",
                form.errors.as_json(),
                user_data,
            )
            return None, "Invalid or expired token"

        except signing.SignatureExpired:
            self.logger.warning("Signature expired for token: %s", self.token)
            return None, "The verification link has expired. Please sign up again."
        except signing.BadSignature:
            self.logger.error("Bad signature for token: %s", self.token)
            return None, "Invalid verification link. Please sign up again."
        except Exception as e:
            self.logger.exception(
                "Unexpected error during token verification: %s", str(e)
            )
            return None, f"Unexpected error: {str(e)}"
