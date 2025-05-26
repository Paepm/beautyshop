from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # fields to be displayed in the admin panel
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_staff', 'is_superuser', 'phone_number', 'post_code', 'country', 'city', 'address',
        'date_of_birth',
    )

    # fields to be displayed in the admin panel
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'email',
                'date_of_birth', 'gender', 'profile_image',
                'country', 'city', 'address', 'post_code',
                'phone_number', 'newsletter_opt_in', 'terms_accepted',
            )
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # fields to be displayed when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'first_name', 'last_name', 'date_of_birth', 'gender',
                'country', 'city', 'address', 'post_code', 'phone_number',
                'newsletter_opt_in', 'terms_accepted',
                'is_staff', 'is_superuser', 'is_active',
            ),
        }),
    )

    search_fields = ('email', 'username', 'first_name', 'last_name', 'country', 'city')
    ordering = ('email',)

