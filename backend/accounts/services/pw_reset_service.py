from django.contrib.auth import get_user_model
from django.core.signing import Signer, BadSignature
from django.conf import settings
from devtools import debug

from emails.enums.email_templates import EmailTemplate
from emails.services.email_service import EmailService
from beautyshop.logging_config import setup_logger


class PwResetService:
    def __init__(self):
        self.signer = Signer()
        self.logger = setup_logger(__name__)
        self.User = get_user_model()

    def send_password_reset_link(self, email: str) -> tuple[bool, str]:
        from django.conf import settings
        print(f"Service: Processing password reset for email: {email}")
        print(f"Email settings - HOST_USER: '{settings.EMAIL_HOST_USER}'")
        print(f"Email settings - DEFAULT_FROM_EMAIL: '{settings.DEFAULT_FROM_EMAIL}'")
        try:
            user = self.User.objects.get(email=email)
        except self.User.DoesNotExist:
            debug("User with email does not exist:", email)
            return False, "User with this email does not exist."

        token = self.signer.sign(user.pk)
        reset_link = self._get_reset_link(token)

        EmailService.send_email(
            template=EmailTemplate.PASSWORD_RESET,
            to_email=user.email,
            context={
                "reset_link": reset_link,
                "name": user.username,
            },
        )
        return True, "Password reset Email sent."

    def reset_password_with_token(
        self, token: str, new_password: str
    ) -> tuple[bool, str]:
        try:
            primary_key = self.signer.unsign(token)
            debug("Primary key from token:", primary_key)
            user = self.User.objects.get(pk=primary_key)

            user.set_password(new_password)
            user.save()

            EmailService.send_email(
                template=EmailTemplate.PASSWORD_RESET_CONFIRMATION,
                to_email=user.email,
                context={
                    "name": user.username,
                },
            )
            return True, "Password successfully reset."

        except BadSignature:
            self.logger.warning("Invalid Token for password reset: %s", token)
            return False, "Invalid or expired token."

        except self.User.DoesNotExist:
            return False, "User not found for the provided token."

        except Exception as e:
            self.logger.exception("Unecpected error during password reset: %s", str(e))
            return False, "Unexpacted error during password reset."

    def _get_reset_link(self, token: str) -> str:
        frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:3000")
        return f"{frontend_url}/password_reset/{token}"

    # DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE
    @staticmethod
    def get_forgotten_password_url(token: str) -> str:
        """
        Generate a forgotten password URL containing the signed token.
        Args:
            token (str): A signed token containing user data.
        Returns:
            str: The full forgotten password URL.
        """
        return f"http://localhost:3000/password_reset/{token}"  # just for dev, is needed because django and react conflict! need to change in production to right url,

    def reset_user_password(self, user_id: str, new_password: str) -> bool:
        """
        Reset the user's password.
        Args:
            user_id (str): The ID of the user whose password is to be reset.
            new_password (str): The new password to set for the user.
        Returns:
            bool: True if the password was successfully reset, False otherwise.
        """
        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            debug("Password successfully reset for user ID", user_id)
            return True
        except User.DoesNotExist:
            debug("User with ID does not exist: ", user_id)
            return False
        except Exception as e:
            debug("Unexpected error when updating password:", e)
