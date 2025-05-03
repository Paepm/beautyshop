from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth import login
from django.contrib import messages
from devtools import debug
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.core import signing

from .forms import CustomLoginForm
from .forms import SignupForm
from . import email_templates



User = get_user_model()

def email_check_sign_up(request):
    error = None

    if request.method == 'POST':
        email = request.POST.get('email')

        if User.objects.filter(email=email).exists():
            error = "Email already exists, try to log in or reset your password."
            return redirect(f"{reverse('accounts:login')}?email={email}")

        else:
            # Redirect to the  sign_up page if the email is not already in use
            return redirect(f"{reverse('accounts:sign_up')}?email={email}")
                            
    return render(request, 'accounts/email_check_sign_up.html', {'error': error})


def signup_view(request: HttpRequest) -> HttpResponse:
    """
    Handle user signup. Do not create a user yet.
    Instead, send a verification email with a signed token containing the user's data.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            # Extract the cleaned form data (but do not save to the DB yet)
            user_data = form.cleaned_data

            # converte date_of_birth (datatype is datetime.date) to string
            user_data['date_of_birth'] = user_data['date_of_birth'].strftime('%Y-%m-%d')

            # sign the user data securley using Django's signer
            token = signing.dumps(user_data)

            # build the verification URL for the email
            verify_url = request.build_absolute_uri(
                reverse('accounts:verify_email', kwargs={'token': token})
            )

            # send the verification email
            send_mail(
                subject=email_templates.EmailTemplate.WELCOME.value['subject'],
                message=email_templates.EmailTemplate.WELCOME.value['message'].format(
                    name=user_data['username'],
                    verification_link=verify_url
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_data['email']],
                fail_silently=False,
                auth_user=settings.EMAIL_HOST_USER,
                auth_password=settings.EMAIL_HOST_PASSWORD,
            )

            messages.success(request, 'Please check your email to verify your account and complete the signup process.')
            return redirect('shop:product_list') # redirect to product list
        
        else:
            # Pre-fill email if passes in the URL (optional)
            email = request.GET.get('email')
            form = SignupForm(initial={'email': email})

    else:
        form = SignupForm() # show empty form for GET requests
        
    return render(request, 'accounts/sign_up.html', {'form': form})


def verify_account_view(request: HttpRequest, token: str) -> HttpResponse:
    """
    This view is triggered when a user clicks the email verification link.
    It tries to decode the signed token and create the user.
    If successful, the user is saved, logged in and redirected.
    """

    try:
        # Try to decode the token to get the original form data
        user_data = signing.loads(token, max_age=60*60*24)  # Token is valid for 24 hours

        # Use the existing SignupForm to validate and create the user
        user_form = SignupForm(user_data)

        if user_form.is_valid():
            # Create the user
            user = user_form.save()
            login(request, user)
            messages.success(request, 'Your account has been verified and you are now logged in.')

            # send a post-verification email
            send_mail(
                subject=email_templates.EmailTemplate.USER_CREATED.value['subject'],
                message=email_templates.EmailTemplate.USER_CREATED.value['message'].format(
                    name=user.username
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
                auth_user=settings.EMAIL_HOST_USER,
                auth_password=settings.EMAIL_HOST_PASSWORD,
            )
            return redirect('shop:product_list')
        else:
            return HttpResponse('Invalid user data in verification link.', status=400)
        
    except signing.SignatureExpired:
        return HttpResponse('The verification link has expired. Please sign up again.', status=400)
    except signing.BadSignature:
        return HttpResponse('Invalid verification link. Please sign up again.', status=400)
    except Exception as e:
        return HttpResponse(f'Unexpected error: {str(e)}', status=500)
            

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('shop:product_list')  # or redirect to a diffrent page
        else:
            messages.error(request, "Login failed. Please check your username/email and password.")
    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form})

