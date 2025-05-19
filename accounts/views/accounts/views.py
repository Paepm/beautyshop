from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib import messages
from devtools import debug
from django.http import HttpRequest, HttpResponse


from ...forms import CustomLoginForm
from ...forms import SignupForm
from ...services.verification_service import EmailVerificationService
from ...services.confirmation_service import EmailConfirmationService
from ...services.login_service import LoginService
from ...forms import CustomLoginForm
from beautyshop.logging_config import setup_logger

User = get_user_model()
logger = setup_logger(__name__)


def email_check_sign_up(request):
    """
    Check if the email is already in use, if so, redirect to login page.
    """
    error = None

    if request.method == "POST":
        email = request.POST.get("email")

        if User.objects.filter(email=email).exists():
            error = "Email already exists, try to log in or reset your password."
            return redirect(f"{reverse('accounts:login')}?email={email}")

        else:
            # Redirect to the  sign_up page if the email is not already in use
            return redirect(f"{reverse('accounts:sign_up')}?email={email}")

    return render(request, "accounts/email_check_sign_up.html", {"error": error})


def signup_view(request: HttpRequest) -> HttpResponse:
    """
    Handle user signup: validate form, send verification email with signed token.
    """
    email = request.GET.get("email", "")

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            reg_service = EmailVerificationService(request, form.cleaned_data)

            if reg_service.prepare_and_send_verification_email():
                messages.success(
                    request, "Please check your email to verify your account."
                )
                return redirect("shop:product_list")
            else:
                messages.error(
                    request, "Could not send verification email. Please try again."
                )

    else:
        form = SignupForm(initial={"email": email})

    return render(request, "accounts/sign_up.html", {"form": form})


def login_view(request):
    """
    Handle user login using username or email and password.
    """
    if request.method == "POST":
        form = CustomLoginForm(request.POST)

        if form.is_valid():
            login_service = LoginService(
                request,
                form.cleaned_data["username_or_email"],
                form.cleaned_data["password"],
            )

            if login_service.authenticate_user():
                login_service.login_user()
                user = login_service.get_user()
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect("shop:product_list")
            else:
                messages.error(request, "Login failed. Please check your credentials.")
    else:
        form = CustomLoginForm()

    return render(request, "accounts/login.html", {"form": form})
