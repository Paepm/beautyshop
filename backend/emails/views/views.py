from django.http import JsonResponse, HttpRequest, HttpResponse
from accounts.services.confirmation_service import EmailConfirmationService
from ..services.email_verification import VerificationEmailService
from ..enums.email_templates import EmailTemplate


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
