from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from accounts.services.login_service import LoginService

# get the user model, which can be the default User or a custom user model
User = get_user_model()


class LoginServiceTestCase(TestCase):
    """
    Unit tests for the LoginService class to verify authentication behavior.
    Covers login via username, email, invalid password, and nonexistent users.
    """

    def setUp(self):
        """
        Prepare test environment before each test method:
        - Create a RequestFactory instance to simulate HTTP requests
        - Create a test user with known credentials for authentication tests
        """
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_login_with_username_success(self):
        """
        Test login with correct username and password.
        Verifies that authentication succeeds and the correct user is returned.
        """
        request = self.factory.post("/login/")
        service = LoginService(request, "testuser", "testpass123")
        authenticated = service.authenticate_user()

        self.assertTrue(authenticated)
        self.assertEqual(service.get_user(), self.user)

    def test_login_with_email_success(self):
        """
        Test login with correct email and password.
        Verifies that authentication succeeds and the correct user is returned.
        """
        request = self.factory.post("/login/")
        service = LoginService(request, "test@example.com", "testpass123")
        authenticated = service.authenticate_user()

        self.assertTrue(authenticated)
        self.assertEqual(service.get_user(), self.user)

    def test_login_failure_wrong_password(self):
        """
        Test login attempt with correct username but wrong password.
        Verifies that authentication fails and no user is returned.
        """
        request = self.factory.post("/login/")
        service = LoginService(request, "testuser", "wrongpass")
        authenticated = service.authenticate_user()

        self.assertFalse(authenticated)
        self.assertIsNone(service.get_user())

    def test_login_failure_nonexistent_user(self):
        """
        Test login attempt with a username/email that does not exist.
        Verifies that authentication fails and no user is returned.
        """
        request = self.factory.post("/login/")
        service = LoginService(request, "unknownuser", "somepass")
        authenticated = service.authenticate_user()

        self.assertFalse(authenticated)
        self.assertIsNone(service.get_user())
