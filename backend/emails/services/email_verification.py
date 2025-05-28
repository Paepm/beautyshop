from django.core.mail import send_mail, BadHeaderError
from smtplib import SMTPException
from django.conf import settings

from beautyshop.logging_config import setup_logger


class VerificationEmailService:

    @staticmethod
    def send_verification_email(email: str, subject: str, message: str) -> None:
        """
        Send a verification email containing a link with the signed token.

        Args:
            email (str): Recipient email address.
            subject (str): Email subject line.
            message (str): The message body.

        Returns:
            None
        """
        logger = setup_logger(__name__)
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
            logger.info("Verification email successfully sent to %s", email)
        except BadHeaderError as e:
            logger.warning(
                "BadHeaderError while sending email to %s: %s", email, str(e)
            )
        except SMTPException as e:
            logger.error("SMTPException while sending email to %s: %s", email, str(e))
        except Exception as e:
            logger.exception(
                "Unexpected error while sending email to %s: %s", email, str(e)
            )

    @staticmethod
    def get_verification_url(token: str) -> str:
        """
        Generate a verification URL containing the signed token.

        Args:
            token (str): A signed token containing user registration data.

        Returns:
            str: The full verification URL.
        """
        return f"http://localhost:3000/verify/{token}"  # just for dev, is needed because django and react conflict! need to change in production to right url,
