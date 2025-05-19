from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages

from emails.enums.email_templates import EmailTemplate


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "emails/password_reset_confirm.html"
    success_url = reverse_lazy("emails:password_reset_complete")

    # to send a confirmation email after the password has been changed
    def form_valid(self, form):
        # override the form_valid method to send a confirmation email
        response = super().form_valid(form)

        user = self.user

        if user and user.email:
            send_mail(
                subject=EmailTemplate.PASSWORD_RESET_CONFIRMATION.value["subject"],
                message=EmailTemplate.PASSWORD_RESET_CONFIRMATION.value[
                    "message"
                ].format(name=user.username),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            messages.success(
                self.request, "Password changed – confirmation email sent."
            )

        return response
