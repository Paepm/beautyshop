from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework import status
from accounts.forms import SignupForm

from accounts.services.confirmation_service import EmailConfirmationService
from emails.enums.email_templates import EmailTemplate
from accounts.services.verification_service import EmailVerificationService
from emails.services.email_verification import VerificationEmailService


class SignupAPIView(APIView):
    """
    Handles user registration via React frontend with email verification.
    """

    def post(self, request):
        form = SignupForm(request.data)

        if form.is_valid():
            service = EmailVerificationService(request, form.cleaned_data)

            if service.prepare_and_send_verification_email():
                return Response(
                    {"message": "Please check your email to verify your account."},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"non_field_errors": ["Could not send verification email."]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def verify_account_view(request: HttpRequest, token: str) -> HttpResponse:
        """
        Handles the email verification by decoding the token, creating the user,
        logging them in and sending a final welcome email.

        Args:
            request (HttpRequest): The incoming HTTP request.
            token (str): A signed token containing user registration data.

        Returns:
            HttpResponse: JSON response with success or error message.
        """
        service = EmailConfirmationService(request, token)
        user, error = service.verify_and_create_user()
        email_template = EmailTemplate

        if user:
            # Sends a final welcome email to the verified user
            VerificationEmailService.send_verification_email(
                user.email,
                subject=email_template.USER_CREATED.value["subject"],
                message=email_template.USER_CREATED.value["message"],
            )

            return JsonResponse({"status": "success", "message": "Account verified."})
        else:
            return JsonResponse(
                {"status": "error", "error": error or "Invalid token"}, status=400
            )
