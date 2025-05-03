from enum import Enum


class EmailTemplate(Enum):
    WELCOME = {
        'subject': 'Welcome to Beautyshop',
        'message': (
            'Hi {name},\n\n'
            'Welcome to Beautyshop! We are glad to have you with us.\n\n'
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