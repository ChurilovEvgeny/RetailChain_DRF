from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.permissions import IsSelfProfile
from users.serializers import (
    UserSerializer,
    UserShortSerializer,
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    @extend_schema(
        summary="Создание пользователя",
        description="Создает нового пользователя.",
        responses={
            200: OpenApiResponse(
                response=UserSerializer, description="Успешный запрос"
            ),
            400: OpenApiResponse(description="Некорректные данные"),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Получение списка зарегистрированных пользователей",
        description="Возвращает список всех изображений зарегистрированных пользователей.",
        responses={
            200: OpenApiResponse(
                response=UserShortSerializer(many=True), description="Успешный ответ"
            ),
            401: OpenApiResponse(description="Необходима авторизация"),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Получение параметров пользователя",
        description="Возвращает параметры пользователя по указанному идентификатору.",
        responses={
            200: OpenApiResponse(response=UserSerializer, description="Успешный ответ"),
            401: OpenApiResponse(description="Необходима авторизация"),
            404: OpenApiResponse(description="Указанный пользователь не существует"),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Обновление пользователя",
        description="Обновляет параметры пользователя по указанному идентификатору.",
        responses={
            200: OpenApiResponse(
                response=UserShortSerializer, description="Успешный ответ"
            ),
            401: OpenApiResponse(description="Необходима авторизация"),
            403: OpenApiResponse(description="Нет доступа"),
            404: OpenApiResponse(description="Указанный пользователь не существует"),
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Частичное обновление пользователя",
        description="Обновляет параметры пользователя по указанному идентификатору.",
        responses={
            200: OpenApiResponse(
                response=UserShortSerializer, description="Успешный ответ"
            ),
            401: OpenApiResponse(description="Необходима авторизация"),
            403: OpenApiResponse(description="Нет доступа"),
            404: OpenApiResponse(description="Указанный пользователь не существует"),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Удаление пользователя",
        description="Удаляет пользователя по указанному идентификатору.",
        responses={
            204: OpenApiResponse(response=None, description="Успешный ответ"),
            401: OpenApiResponse(description="Необходима авторизация"),
            403: OpenApiResponse(description="Нет доступа"),
            404: OpenApiResponse(description="Указанный пользователь не существует"),
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_object(self):
        obj = super().get_object()
        # Специально сохраняем получаемый объект,
        # для получения нужного сериализатора
        self.user_obj = obj
        return obj

    def get_serializer_class(self):
        if self.action == "list":
            return UserShortSerializer
        elif self.action == "retrieve":
            # Выбираем нужный сериализатор, исходя из совпадающего pk
            if self.request.user == self.user_obj:
                return UserSerializer
            else:
                return UserShortSerializer
        return UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [
                AllowAny,
            ]
        elif self.action in ("list", "retrieve"):
            self.permission_classes = [
                IsAuthenticated,
            ]
        else:
            self.permission_classes = [
                IsSelfProfile,
            ]
        return super().get_permissions()
