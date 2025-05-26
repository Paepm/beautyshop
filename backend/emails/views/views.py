from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpRequest, HttpResponse

from accounts.services.confirmation_service import EmailConfirmationService


# Create your views here.
def verify_account_view(request: HttpRequest, token: str) -> HttpResponse:
    """
    Handles the email verification by decoding the token and creating the user.
    """
    service = EmailConfirmationService(request, token)
    user, error = service.verify_and_create_user()

    if user:
        messages.success(
            request, "Your account has been verified and you're logged in."
        )
        return redirect("shop:product_list")
    else:
        return HttpResponse(error or "Unexpected error", status=400)
