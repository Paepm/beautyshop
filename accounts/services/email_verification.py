from django.core import signing
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpRequest
from typing import Optional, Tuple

from accounts.forms import SignupForm
from accounts.email_templates import EmailTemplate
from accounts.models import CustomUser


class EmailVerificationService:
    """
    Service for verifying a signed signup token, creating a new user, and sending a confirmation email.
    """

    def __init__(self, request: HttpRequest, token: str):
        """
        Initialize the service with the HTTP request and the signed token.

        Args:
            request (HttpRequest): The incoming request.
            token (str): The signed string containing user data.
        """
        self.request = request
        self.token = token

    def verify_and_create_user(self) -> Tuple[Optional[CustomUser], Optional[str]]:
        """
        Verifies the signed token, validates the data, creates a new user, logs them in,
        and sends a confirmation email.

        Returns:
            Tuple[Optional[CustomUser], Optional[str]]: A tuple where the first element is the created user
            (or None if creation failed), and the second element is an error message (or None if successful).
        """
        try:
            user_data = signing.loads(self.token, max_age=60 * 60 * 24)
            form = SignupForm(user_data)

            if form.is_valid():
                user = form.save()
                login(self.request, user)
                self.send_confirmation_email(user)
                return user, None
            return None, "Invalid or expired token"

        except signing.SignatureExpired:
            return None, "The verification link has expired. Please sign up again."
        except signing.BadSignature:
            return None, "Invalid verification link. Please sign up again."
        except Exception as e:
            return None, f"Unexpected error: {str(e)}"

    def send_confirmation_email(self, user: CustomUser) -> None:
        """
        Sends a welcome email to the newly created user after successful verification.

        Args:
            user (CustomUser): The newly created and logged-in user.

        Returns:
            None
        """
        send_mail(
            subject=EmailTemplate.USER_CREATED.value['subject'],
            message=EmailTemplate.USER_CREATED.value['message'].format(name=user.username),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
            auth_user=settings.EMAIL_HOST_USER,
            auth_password=settings.EMAIL_HOST_PASSWORD,
        )
