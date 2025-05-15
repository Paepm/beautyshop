from enum import Enum


class EmailTemplate(Enum):
    WELCOME = {
        'subject': 'Verify your Beautyshop account',
        'message': (
            'Hi {name},\n\n'
            'Welcome to Beautyshop! We are glad to have you with us.\n\n'
            'Please verify your email address by clicking the link below:\n'
            '{verification_link}\n\n'
            'If you did not sign up for this account, please ignore this email.\n\n'
            'Best regards,\n'
            'Beautyshop Team'
        )
    }

    USER_CREATED = {
        'subject': 'Your Beautyshop account has been created',
        'message': (
            'Hi {name},\n\n'
            'Congratulations! Your Beautyshop account has been successfully created.\n\n'
            'You can now log in and start shopping.\n\n'
            'Best regards,\n'
            'Beautyshop Team'
        )
    }

    ORDER_CONFIRMATION = {
        'subject': 'Your order at Beautyshop',
        'message': (
            'Hi {name},\n\n'
            'We received your order and will process it shortly.\n\n'
            'Best regards,\n'
            'Beautyshop Team'
        )
    }

    