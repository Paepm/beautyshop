from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth import login
from django.contrib import messages
from devtools import debug

from .forms import CustomLoginForm
from .forms import SignupForm



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

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        debug(form.errors)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shop:product_list')  # or redirect to a different page
    else:
        email = request.GET.get('email', '')
        form = SignupForm(initial={'email': email})
        debug(form)
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

