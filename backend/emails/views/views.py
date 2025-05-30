from django.http import JsonResponse, HttpRequest, HttpResponse
from django.contrib.auth import get_user_model
from devtools import debug
from django.core.signing import Signer

from accounts.services.confirmation_service import EmailConfirmationService
from ..services.email_verification import VerificationEmailService
from ..services.email_forgotten_password import EmailForgottenPasswordService
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


def forgotten_password_view(request: HttpRequest) -> HttpResponse:
    """
    Handles the password reset email request.
    """
    email = request.POST.get("email")
    debug("Received email for password reset", email)

    if not email:
        return JsonResponse(
            {"status": "error", "message": "Email is required"}, status=400
        )

    # get the user model --> later find the right user by email
    User = get_user_model()
    debug("USER_MODEL: %s", User)

    try:
        user = User.objects.get(email=email)
        debug("USER_FOUND:", user)
    except User.DoesNotExist:
        debug("No user found with email:", email)
        return JsonResponse(
            {"status": "error", "message": "No user with this email"}, status=404
        )

    # generate a signed token for the user
    signer = Signer()
    token = signer.sign(user.pk)

    # send an email with the reset password link
    service = EmailForgottenPasswordService()
    service.send_reset_password_email(
        email=user.email,
        subject=EmailTemplate.PASSWORD_RESET.value["subject"],
        message=EmailTemplate.PASSWORD_RESET.value["message"].format(
            reset_link=service.get_forgotten_password_url(token), name=user.first_name
        ),
    )
    return JsonResponse({"status": "success", "message": "Password reset email sent."})


def reset_password_view(request: HttpRequest) -> HttpResponse:
    """ """

    pass
