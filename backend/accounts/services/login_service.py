from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpRequest
from typing import Optional

from accounts.models import CustomUser  # falls du ein CustomUser-Modell verwendest

User = get_user_model()


class LoginService:
    """
    Handles user authentication and login logic.
    Supports login via username or email.
    """

    def __init__(self, request: HttpRequest, username_or_email: str, password: str):
        """
        Initialize the login service with the current request and credentials.

        Args:
            request (HttpRequest): The incoming HTTP request.
            username_or_email (str): The username or email address entered by the user.
            password (str): The user's password.
        """
        self.request = request
        self.username_or_email = username_or_email
        self.password = password
        self.user: Optional[CustomUser] = None

    def authenticate_user(self) -> bool:
        """
        Try to authenticate the user using the provided username or email and password.

        Returns:
            bool: True if authentication was successful, False otherwise.
        """
        try:
            user = User.objects.filter(email=self.username_or_email).first()
            username = user.username if user else self.username_or_email
        except Exception:
            username = self.username_or_email

        self.user = authenticate(username=username, password=self.password)
        return self.user is not None

    def login_user(self) -> None:
        """
        Log the user into the current session if authentication was successful.

        Returns:
            None
        """
        if self.user:
            login(self.request, self.user)

    def get_user(self) -> Optional[CustomUser]:
        """
        Get the authenticated user object, if available.

        Returns:
            Optional[CustomUser]: The authenticated user, or None if not authenticated.
        """
        return self.user
