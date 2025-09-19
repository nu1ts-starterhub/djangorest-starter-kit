from django.contrib.auth import get_user_model
from django.db import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auth_app.serializers import RegisterRequestSerializer, LoginRequestSerializer
from apps.auth_app.serializers_response import RegisterResponseSerializer, ErrorResponseSerializer, LoginResponseSerializer
from core.mixins import ErrorResponseMixin

User = get_user_model()

class RegisterView(ErrorResponseMixin, APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        tags=['auth'],
        operation_summary="Регистрация пользователя",
        operation_description="Создает нового пользователя и возвращает токены",
        request_body=RegisterRequestSerializer,
        responses={
            200: openapi.Response(
                description="Успешная регистрация",
                schema=RegisterResponseSerializer
            ),
            400: openapi.Response(
                description="Некорректные данные или пользователь уже существует",
                schema=ErrorResponseSerializer
            ),
            500: openapi.Response(
                description="Внутренняя ошибка сервера",
                schema=ErrorResponseSerializer
            ),
        },
    )
    def post(self, request):
        serializer = RegisterRequestSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }, status=status.HTTP_200_OK)
        except IntegrityError:
            return ErrorResponseMixin.format_error(request, status.HTTP_400_BAD_REQUEST,"Bad Request",
                "User with this username or email already exists."
            )



class LoginView(ErrorResponseMixin, APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['auth'],
        operation_summary="Авторизация пользователя",
        operation_description="Принимает email и password, возвращает access и refresh токены",
        request_body=LoginRequestSerializer,
        responses={
            200: openapi.Response(
                description="Успешная авторизация",
                schema=LoginResponseSerializer
            ),
            400: openapi.Response(
                description="Неверный email или пароль",
                schema=ErrorResponseSerializer
            ),
            401: openapi.Response(
                description="Неверные учетные данные",
                schema=ErrorResponseSerializer
            ),
            500: openapi.Response(
                description="Внутренняя ошибка сервера",
                schema=ErrorResponseSerializer
            ),
        },
    )
    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return ErrorResponseMixin.format_error(
                request,
                status.HTTP_400_BAD_REQUEST,
                "Bad Request",
                serializer.errors
            )

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return ErrorResponseMixin.format_error(
                request,
                status.HTTP_401_UNAUTHORIZED,
                "Unauthorized",
                "User not found"
            )

        if not user.check_password(password):
            return ErrorResponseMixin.format_error(
                request,
                status.HTTP_401_UNAUTHORIZED,
                "Unauthorized",
                "Invalid email or password"
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)