from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth import login
from django.contrib import messages
from devtools import debug
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpRequest, HttpResponse

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
    print("USERNAME:", settings.EMAIL_HOST_USER)
    print("PASSWORD:", settings.EMAIL_HOST_PASSWORD)
    # Load welcome message from email templates
    message = email_templates.EmailTemplate.WELCOME.value
    debug(type(message['subject']))  # Debug: confirm it's a string
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        debug(form.errors)  # Log any validation errors

        # Check if the submitted form is valid
        if form.is_valid():
            user = form.save()

            # Send welcome email with dynamic user name
            send_mail(
                subject=message['subject'].format(name=form.cleaned_data['first_name']),    # format str is needed to replace {name} with the actual name
                message=message['message'].format(name=form.cleaned_data['first_name']),    # format str is needed to replace {name} with the actual name
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
                auth_user='mair.patrick@gmx.at',
                auth_password='O63UTWLJ2WQ56YFSM4K6',
            )

            # Log the user in and redirect to product list
            login(request, user)
            return redirect('shop:product_list')

    else:
        # If request is GET, show empty form (optionally pre-filled with email from URL)
        email = request.GET.get('email', '')
        form = SignupForm(initial={'email': email})
        debug(form)

    # Render the signup form template with the current form state
    return render(request, 'accounts/sign_up.html', {'form': form})

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

