from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import SelectDateWidget
from datetime import date

from .models import CustomUser


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    terms_accepted = forms.BooleanField(
        required=True, label="I accept the terms and conditions"
    )
    date_of_birth = forms.DateField(
        widget=SelectDateWidget(years=range(1900, date.today().year + 1)),
        required=True,
        label="Date of Birth",
    )

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "profile_image",
            "username",
            "email",
            "password1",
            "password2",
            "country",
            "city",
            "address",
            "post_code",
            "phone_number",
            "newsletter_opt_in",
            "terms_accepted",
        ]
