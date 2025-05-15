from django.core import signing
from django.urls import reverse
from django.core.mail import send_mail, BadHeaderError
from smtplib import SMTPException
from django.conf import settings
from django.http import HttpRequest

from accounts.enums.email_templates import EmailTemplate
from beautyshop.logging_config import setup_logger


class RegistrationService:
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
            token = self.generate_signed_token()
            verification_url = self.get_verification_url(token)

            subject = EmailTemplate.WELCOME.value['subject']
            message = EmailTemplate.WELCOME.value['message'].format(
                name=self.form_data['username'],
                verification_link=verification_url
            )

            self._send_verification_email(
                email=self.form_data['email'],
                subject=subject,
                message=message
            )
            return True

        except Exception as e:
            self.logger.exception("Failed to send verification email: %s", str(e))
            return False


    def generate_signed_token(self) -> str:
        """
        Create a signed token from the user's form data for secure email verification.

        Returns:
            str: A signed string token containing the user data.
        """
        data = self.form_data.copy()
        data['date_of_birth'] = data['date_of_birth'].strftime('%Y-%m-%d')      # Convert date to string
        return signing.dumps(data)

    def get_verification_url(self, token: str) -> str:
        """
        Build the full verification URL using the signed token.

        Args:
            token (str): The signed token representing the user data.

        Returns:
            str: The full verification URL to be sent via email.
        """
        return self.request.build_absolute_uri(
            reverse('accounts:verify_email', kwargs={'token': token})
        )

    def _send_verification_email(self, email: str, subject: str, message: str) -> None:
        """
        Send a verification email containing a link with the signed token.

        Args:
            email (str): Recipient email address.
            subject (str): Email subject line.
            message (str): The message body.

        Returns:
            None
        """

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.form_data['email']],
                fail_silently=False,
                auth_user=settings.EMAIL_HOST_USER,
                auth_password=settings.EMAIL_HOST_PASSWORD,
            )
            self.logger.info("Verification email successfully sent to %s", email)
        except BadHeaderError as e:
            self.logger.warning("BadHeaderError while sending email to %s: %s", email, str(e))
        except SMTPException as e:
            self.logger.error("SMTPException while sending email to %s: %s", email, str(e))
        except Exception as e:
            self.logger.exception("Unexpected error while sending email to %s: %s", email, str(e))
