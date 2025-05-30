from django.core.mail import send_mail, BadHeaderError
from smtplib import SMTPException
from django.conf import settings
from devtools.debug import debug


class EmailForgottenPasswordService:
    """
    Service for sending forgotten password emails.
    """

    @staticmethod
    def get_forgotten_password_url(token: str) -> str:
        """
        Generate a forgotten password URL containing the signed token.

        Args:
            token (str): A signed token containing user data.

        Returns:
            str: The full forgotten password URL.
        """
        return f"http://localhost:3000/password_reset//{token}"  # just for dev, is needed because django and react conflict! need to change in production to right url,

    @staticmethod
    def send_reset_password_email(email: str, subject: str, message: str) -> None:
        """
        Send a email containing a link with the url to the reset password page.

        Args:
            email (str): Recipient email address.
            subject (str): Email subject line.
            message (str): The message body.

        Returns:
            None
        """
        # logger = setup_logger(__name__)
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
                auth_user=settings.EMAIL_HOST_USER,
                auth_password=settings.EMAIL_HOST_PASSWORD,
            )
            debug("Verification email successfully sent to %s", email)
        except BadHeaderError as e:
            debug("BadHeaderError while sending email to %s: %s", email, str(e))
        except SMTPException as e:
            debug("SMTPException while sending email to %s: %s", email, str(e))
        except Exception as e:
            debug("Unexpected error while sending email to %s: %s", email, str(e))
