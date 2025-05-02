from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('email_check_sign_up', views.email_check_sign_up, name='email_check_sign_up'),
    path('sign_up', views.signup_view, name='sign_up'),
    
]