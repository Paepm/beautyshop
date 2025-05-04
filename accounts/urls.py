from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    path('email_check_sign_up/', views.email_check_sign_up, name='email_check_sign_up'),
    path('sign_up/', views.signup_view, name='sign_up'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='shop:product_list') , name='logout'),
    path('verify_email/<str:token>/', views.verify_account_view, name='verify_email'),
    path('password_reset_email/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset_email'),
    path('password_reset_confirm/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    
]