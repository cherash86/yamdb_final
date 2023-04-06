from rest_framework import serializers
from users import validators
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        allow_blank=False,
        validators=[validators.email_validation]
    )
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        allow_blank=False,
        validators=[validators.username_validation]
    )

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        allow_blank=False,
        validators=[validators.email_validation]
    )
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        validators=[validators.username_validation],
        max_length=150
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'username')


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        validators=[validators.user_validation]
    )

    class Meta:
        model = CustomUser
        fields = ('username',)


class UserSelfSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        allow_blank=True,
        max_length=150
    )
    last_name = serializers.CharField(
        allow_blank=True,
        max_length=150
    )
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150
    )

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)
