from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.forms.widgets import SelectDateWidget
from datetime import date
import datetime

from django.contrib.auth import get_user_model
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'date_of_birth', 'gender', 'profile_image', 'username', 'email', 'password1', 'password2',
                   'country', 'city', 'address', 'post_code', 'phone_number', 'newsletter_opt_in', 'terms_accepted')


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    terms_accepted = forms.BooleanField(required=True, label="I accept the terms and conditions")
    date_of_birth = forms.DateField(
        widget=SelectDateWidget(years=range(1900, date.today().year + 1)),
        required=True,
        label="Date of Birth"
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender', 'profile_image',
            'username', 'email', 'password1', 'password2', 'country', 'city',
            'address', 'post_code', 'phone_number', 'newsletter_opt_in', 'terms_accepted'
        ]

class CustomLoginForm(forms.Form):
    username_or_email = forms.CharField(label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        """Validate the form data and authenticate the user."""
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')

        User = get_user_model()

        try:
            # search for user by email
            user = User.objects.get(email=username_or_email)
            username = user.username
        except User.DoesNotExist:
            username = username_or_email  # fallback at username

        self.user = authenticate(username=username, password=password)

        if self.user is None:
            raise forms.ValidationError("Invalid username/email or password.")

        return cleaned_data

    def get_user(self):
        return self.user
    

class ProfileEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(
            years=range(datetime.date.today().year - 30, datetime.date.today().year + 1)
        )
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email',
            'phone_number', 'address', 'post_code',
            'city', 'country', 'date_of_birth',
            'gender', 'profile_image',
            'newsletter_opt_in'
        ]