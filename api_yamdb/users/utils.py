from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken


def send_confirmation_code(
    email: str,
    confirmation_code: str,
    username
) -> None:
    """Отправляет код подтверждения пользователю."""
    send_mail(
        'Код подтверждения',
        f'Здравствуйте, {username}! Ваш код: {confirmation_code}',
        from_email='cherash1234@.ru',
        recipient_list=[email],
        fail_silently=False,
    )


def get_tokens_for_user(user):
    """Создаёт токен вручную."""
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
