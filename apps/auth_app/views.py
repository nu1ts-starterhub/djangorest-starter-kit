from django.db import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auth_app.serializers import RegisterSerializer
from apps.auth_app.serializers_response import RegisterResponseSerializer, ErrorResponseSerializer
from core.mixins import ErrorResponseMixin


class RegisterView(ErrorResponseMixin, APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        tags=['auth'],
        operation_summary="Регистрация пользователя",
        operation_description="Создает нового пользователя и возвращает токены",
        request_body=RegisterSerializer,
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
        serializer = RegisterSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }, status=status.HTTP_200_OK)
        except IntegrityError:
            return ErrorResponseMixin.format_error(request, status.HTTP_400_BAD_REQUEST,"IntegrityError",
                "User with this username or email already exists."
            )
