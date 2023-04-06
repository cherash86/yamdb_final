from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import CustomUser
from .permissions import Admin, Superuser
from .serializers import CustomUserSerializer, SignUpSerializer
from .serializers import TokenSerializer, UserSelfSerializer
from .utils import send_confirmation_code, get_tokens_for_user


class UserViewSet(viewsets.ModelViewSet):
    """Получить список всех пользователей или добавить пользователя."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [Admin | Superuser]
    lookup_field = 'username'
    search_field = ('username',)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        serializer_class = UserSelfSerializer

        if request.method == 'GET':
            serializer = serializer_class(user)
            return Response(serializer.data)

        serializer = serializer_class(user, partial=True, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    email = request.data.get('email')
    username = request.data.get('username')
    user = CustomUser.objects.filter(username=username, email=email).exists()
    if not user:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = CustomUser.objects.get(username=username, email=email)
        confirmation_code = default_token_generator.make_token(user)
        send_confirmation_code(email, confirmation_code, username)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response('Пользователь создан!', status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = request.data.get('username')
    user = get_object_or_404(CustomUser, username=username)
    confirmation_code = request.data.get('confirmation_code')
    if default_token_generator.check_token(user, confirmation_code):
        token = get_tokens_for_user(user)
        response = {'token': str(token['access'])}
        return Response(response, status=status.HTTP_200_OK)
    return Response('Проверочный код не совпал',
                    status=status.HTTP_400_BAD_REQUEST)
