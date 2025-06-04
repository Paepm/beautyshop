from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from smtplib import SMTPException

from emails.enums.email_templates import EmailTemplate
from beautyshop.logging_config import setup_logger


class EmailService:

    @staticmethod
    def send_email(template: EmailTemplate, to_email: str, context: dict) -> None:
        logger = setup_logger(__name__)
        try:
            subject = template.value["subject"]
            message = template.value["message"].format(**context)

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[to_email],
                fail_silently=False,
                auth_user=settings.EMAIL_HOST_USER,
                auth_password=settings.EMAIL_HOST_PASSWORD,
            )
            logger.info("email [%s] sent successfully to %s", template.name, to_email)

        except BadHeaderError as e:
            logger.warning(
                "BadHeaderError while sending email to %s: %s", to_email, str(e)
            )
        except SMTPException as e:
            logger.error(
                "SMTPException while sending email to %s: %s", to_email, str(e)
            )
        except Exception as e:
            logger.exception(
                "Unexpected error while sending email to %s: %s", to_email, str(e)
            )
