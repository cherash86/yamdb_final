from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Расширение модели User полями bio и role.
    Определение вариантов и имен для каждого варианта внутри класса модели
    сохраняет всю эту информацию вместе с классом, который его использует,
    и помогает ссылаться на варианты (например, CustomUser.ADMIN
    будет работать везде, где была импортирована модель CustomUser)
    """
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    CHOISES = [
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]

    username: str = models.CharField(
        'Username',
        unique=True,
        max_length=150,
    )
    email: str = models.EmailField(
        'E-mail address',
        unique=True,
        blank=False,
        max_length=254,
    )
    role: str = models.CharField(
        max_length=9,
        choices=CHOISES,
        default='user'
    )
    bio: str = models.TextField(
        'Биография пользователя',
        blank=True
    )
    first_name: str = models.CharField(
        'first name',
        max_length=150,
        blank=True
    )
    last_name: str = models.CharField(
        'last name',
        max_length=150,
        blank=True
    )

    class Meta:
        ordering = ('role',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_name'
            ),
        ]

    @property
    def is_moderator(self):
        return self.role == CustomUser.MODERATOR

    @property
    def is_admin(self):
        return self.role == CustomUser.ADMIN

    @property
    def is_user(self):
        return self.role == CustomUser.USER
