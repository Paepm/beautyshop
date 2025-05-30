from django.contrib.auth import get_user_model
from devtools import debug
from django.core.signing import Signer
from django.http import JsonResponse, HttpRequest, HttpResponse
import json

from emails.enums.email_templates import EmailTemplate
from emails.services.email_forgotten_password import EmailForgottenPasswordService
from accounts.services.forgot_pw_service import ForgotPasswordService


def reset_password_view(request: HttpRequest, token: str) -> HttpResponse:
    """"""
    # get the new selected password from the user
    data = json.loads(request.body)
    new_password = data.get("password")
    debug("NEUES PASSWORT:", new_password)

    signer = Signer()
    User = get_user_model()

    user_id = signer.unsign(token)

    user = User.objects.get(id=user_id)
    debug("USER_FOUND:", user)

    debug("No user found with email:", user.email)

    try:
        user_id = signer.unsign(token)
        debug("User ID from token:", user_id)

    except:
        debug("Invalid token provided for password reset")
        return JsonResponse(
            {"status": "error", "message": "Invalid or expired token"}, status=400
        )
    email_service = EmailForgottenPasswordService()
    service = ForgotPasswordService()
    success = service.reset_user_password(user_id, new_password)

    email_service.send_reset_password_email(
        email=user.email,
        subject=EmailTemplate.PASSWORD_RESET_CONFIRMATION.value["subject"],
        message=EmailTemplate.PASSWORD_RESET_CONFIRMATION.value["message"].format(
            name=user.first_name
        ),
    )

    if success:
        return JsonResponse(
            {"status": "success", "message": "Password reset successfully."}
        )
    else:
        return JsonResponse(
            {"status": "error", "message": "Failed to reset password"}, status=500
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

    # get services
    service = ForgotPasswordService()
    email_service = EmailForgottenPasswordService()

    email_service.send_reset_password_email(
        email=user.email,
        subject=EmailTemplate.PASSWORD_RESET.value["subject"],
        message=EmailTemplate.PASSWORD_RESET.value["message"].format(
            reset_link=service.get_forgotten_password_url(token), name=user.first_name
        ),
    )
    return JsonResponse({"status": "success", "message": "Password reset email sent."})
