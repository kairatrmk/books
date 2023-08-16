from django.core.mail import send_mail


def send_confirmation_email(email, code):
    full_link = f'http://localhost:8000/api/v1/account/activate/{code}'
    send_mail(
        'User activation',
        full_link,
        'exchange.innovat@gmail.com',
        [email]
    )

