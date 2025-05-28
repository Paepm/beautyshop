from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.forms import SignupForm
from accounts.services.verification_service import EmailVerificationService


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
