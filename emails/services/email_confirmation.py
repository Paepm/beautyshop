# emails/services/registration_email_service.py

from django.core.mail import send_mail, BadHeaderError
from smtplib import SMTPException
from django.conf import settings


from accounts.models import CustomUser
from emails.enums.email_templates import EmailTemplate
from beautyshop.logging_config import setup_logger


class ConfirmationEmailService:
    """
    Sends a confirmation email to a user after successful registration.
    """

    @staticmethod
    def send_confirmation_email(user: CustomUser) -> None:
        """
        Sends a welcome email to the newly created user after successful verification. if could not send email, log the error.

        Args:
            user (CustomUser): The newly created and logged-in user.

        Returns:
            None
        """
        logger = setup_logger(__name__)
        try:
            send_mail(
                subject=EmailTemplate.USER_CREATED.value["subject"],
                message=EmailTemplate.USER_CREATED.value["message"].format(
                    name=user.username
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
                auth_user=settings.EMAIL_HOST_USER,
                auth_password=settings.EMAIL_HOST_PASSWORD,
            )
        except BadHeaderError as e:
            logger.warning(
                "BadHeaderError while sending email to %s: %s", user.email, str(e)
            )
        except SMTPException as e:
            logger.error(
                "SMTPException while sending email to %s: %s", user.email, str(e)
            )
        except Exception as e:
            logger.exception(
                "Unexpected error while sending email to %s: %s", user.email, str(e)
            )
