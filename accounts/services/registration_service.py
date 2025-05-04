from django.core import signing
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpRequest

from accounts.email_templates import EmailTemplate


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

    def generate_signed_token(self) -> str:
        """
        Create a signed token from the user's form data for secure email verification.

        Returns:
            str: A signed string token containing the user data.
        """
        data = self.form_data.copy()
        data['date_of_birth'] = data['date_of_birth'].strftime('%Y-%m-%d')
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

    def send_verification_email(self, token: str) -> None:
        """
        Send a verification email containing a link with the signed token.

        Args:
            token (str): The signed user token to be embedded in the email link.

        Returns:
            None
        """
        verification_url = self.get_verification_url(token)

        send_mail(
            subject=EmailTemplate.WELCOME.value['subject'],
            message=EmailTemplate.WELCOME.value['message'].format(
                name=self.form_data['username'],
                verification_link=verification_url
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.form_data['email']],
            fail_silently=False,
            auth_user=settings.EMAIL_HOST_USER,
            auth_password=settings.EMAIL_HOST_PASSWORD,
        )
