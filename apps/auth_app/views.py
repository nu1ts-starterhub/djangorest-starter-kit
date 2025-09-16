from django.db import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auth_app.serializers import RegisterSerializer
from core.mixins import ErrorResponseMixin


class RegisterView(ErrorResponseMixin, APIView):
    @swagger_auto_schema(
        operation_summary="Регистрация пользователя",
        operation_description="Создает нового пользователя и возвращает токены",
        request_body=RegisterSerializer,
        responses={200: openapi.Response("OK")},
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
