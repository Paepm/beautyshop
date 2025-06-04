from django.core import signing
from django.http import HttpRequest
from typing import Optional, Tuple
from django.contrib.auth import login

from accounts.models import CustomUser
from accounts.forms import SignupForm
from emails.enums.email_templates import EmailTemplate
from beautyshop.logging_config import setup_logger
from backend.emails.services.email_service import EmailService


class SignupService:
    """
    Service responsible for preparing and sending a verification email during the user signup process.
    """

    def __init__(self, request: HttpRequest, form_data: dict):
        """
        Initialize the RegistrationService with the request context and form data.

        Args:
            request (HttpRequest): The current HTTP request, used to build absolute URLs.
            form_data (dict): The cleaned signup form data, including user credentials.
        """
        self.request = request
        self.form_data = form_data
        self.logger = setup_logger(__name__)

    def prepare_and_send_verification_email(self) -> bool:
        """
        Builds the verification email and sends it using a secure token.

        Returns:
            bool: True if sending was successful, False otherwise.
        """
        try:
            token = self._generate_signed_token()
            verification_url = self._get_verification_url(token)

            EmailService.send_email(
                template=EmailTemplate.WELCOME,
                to_email=self.form_data["email"],
                context={
                    "name": self.form_data["username"],
                    "verification_link": verification_url,
                },
            )
            return True

        except Exception as e:
            self.logger.exception("Failed to send verification email: %s", str(e))
            return False

    def send_final_welcome_email(self, user: CustomUser) -> None:
        """
        Sends the final welcome email after successful account verification.
        """
        EmailService.send_email(
            template=EmailTemplate.USER_CREATED,
            to_email=user.email,
            context={"name": user.username},
        )

    def verify_and_create_user(
        self, token: str
    ) -> Tuple[Optional[CustomUser], Optional[str]]:
        """
        Decodes the token, validates the data, and creates a new user.

        Returns:
            (user, error message)
        """
        try:
            user_data = signing.loads(token, max_age=60 * 60 * 24)
            form = SignupForm(user_data)

            if form.is_valid():
                user = form.save()
                login(self.request, user)
                return user, None
            else:
                self.logger.warning("Form invalid: %s", form.errors)
                return None, "Invalid registration data."

        except signing.BadSignature:
            return None, "Invalid or tampered token."
        except signing.SignatureExpired:
            return None, "Token has expired."
        except Exception as e:
            self.logger.exception("Unexpected error during verification: %s", str(e))
            return None, "Unexpected error."

    def _generate_signed_token(self) -> str:
        """
        Create a signed token from the user's form data for secure email verification.

        Returns:
            str: A signed string token containing the user data.
        """
        data = self.form_data.copy()
        data["date_of_birth"] = data["date_of_birth"].strftime(
            "%Y-%m-%d"
        )  # Convert date to string
        return signing.dumps(data)

    @staticmethod
    def _get_verification_url(token: str) -> str:
        """
        Generate a verification URL containing the signed token.

        Args:
            token (str): A signed token containing user registration data.

        Returns:
            str: The full verification URL.
        """
        return f"http://localhost:3000/verify/{token}"  # just for dev, is needed because django and react conflict! need to change in production to right url,
