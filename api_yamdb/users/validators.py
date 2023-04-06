from rest_framework.exceptions import ValidationError
from users.models import CustomUser
from rest_framework import status
from rest_framework.response import Response


def username_validation(value):
    """Проверка имени пользователя."""
    if value.lower() == 'me':
        raise ValidationError('Недопустимое имя пользователя!')
    elif CustomUser.objects.filter(username__iexact=value).exists():
        raise ValidationError(f'Пользователь с именем {value} '
                              'уже зарегистрирован!')


def email_validation(value):
    """Проверка адреса электронной почты пользователя."""
    if CustomUser.objects.filter(email__iexact=value).exists():
        raise ValidationError(f'Пользователь с почтой {value} '
                              'уже зарегистрирован!')


def user_validation(value):
    """Проверка наличия пользователя."""
    if not CustomUser.objects.filter(username=value).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
