from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.models import User

# from .forms import SignupForm



User = get_user_model()

def email_check_sign_up(request):
    error = None

    if request.method == 'POST':
        email = request.POST.get('email')

        if User.objects.filter(email=email).exists():
            error = "Email already exists, try to log in or reset your password."

        else:
            # Redirect to the sign-up page if the email is not already in use
            return redirect(f"{reverse('accounts:sign_up')}?email={email}")
                            
    return render(request, 'accounts/email_check_sign_up.html', {'error': error})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shop:index')
    else:
        form = SignupForm()
    return render(request, 'accounts/sign_up.html', {'form': form})