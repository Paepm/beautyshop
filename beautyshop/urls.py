"""
URL configuration for beautyshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from beautyshop.settings import BASE_DIR
from django.contrib.auth import views as auth_views

import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls', namespace='shop')),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='shop/logout.html'), name='logout'),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    # paths for django password resetter --> is global needed that it works....
    path('accounts/password_reset_confirm/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password_reset_done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done',),
    path('accounts/password_reset_complete/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_complete'),

]

# for the template static files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(BASE_DIR, 'static'))

# for the media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
