from django.contrib.auth import get_user_model
from devtools import debug


class ForgotPasswordService:

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
