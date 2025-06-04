from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework import status
from accounts.forms import SignupForm

from backend.accounts.services.signup_service import SignupService


class SignupAPIView(APIView):
    """
    Handles user registration via React frontend with email verification.
    """

    def post(self, request):
        form = SignupForm(request.data)

        if form.is_valid():
            service = SignupService(request, form.cleaned_data)

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


class VerifyAccountAPIView(APIView):

    def get(self, request, token: str):
        service = SignupService(request, form_data={})
        user, error = service.verify_and_create_user(token)

        if user:
            service.send_final_welcome_email(user)
            return JsonResponse({"status": "success", "message": "Account verified."})
        return JsonResponse(
            {"status": "error", "message": error or "invalid token"}, status=400
        )

    def post(self, request: HttpRequest, token: str) -> HttpResponse:
        service = SignupService(request, form_data={})  # no form data needed here
        user, error = service.verify_and_create_user(token)

        if user:
            service.send_final_welcome_email(user)
            return JsonResponse({"status": "success", "message": "Account verified."})

        return JsonResponse(
            {"status": "error", "message": error or "invalid token"},
            status=status.HTTP_400_BAD_REQUEST,
        )
