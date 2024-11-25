from django.db.models.functions import Lower
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from retail.models import ChainLink, Contact, Product
from retail.serializers import (
    ChainLinkSerializer,
    ContactSerializer,
    ProductSerializer,
    ChainLinkUpdateSerializer,
)


class ContactsViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Создание контакта",
        description="Создает нового контакта.",
        responses={
            200: OpenApiResponse(
                response=ContactSerializer, description="Успешный запрос"
            ),
            400: OpenApiResponse(description="Некорректные данные"),
            401: OpenApiResponse(description="Необходима авторизация"),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Получение списка контактов",
        description="Возвращает список всех контактов.",
        responses={
            200: OpenApiResponse(
                response=ContactSerializer(many=True), description="Успешный ответ"
            ),
            401: OpenApiResponse(description="Необходима авторизация"),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Получение контакта",
        description="Возвращает контакт по указанному идентификатору.",
        responses={
            200: OpenApiResponse(
                response=ContactSerializer, description="Успешный ответ"
            ),
            401: OpenApiResponse(description="Необходима авторизация"),
            404: OpenApiResponse(description="Указанный контакт не существует"),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Обновление контакта",
        description="Обновляет контакта по указанному идентификатору.",
        responses={
            200: OpenApiResponse(
                response=ContactSerializer, description="Успешный ответ"
            ),
            401: OpenApiResponse(description="Необходима авторизация"),
            404: OpenApiResponse(description="Указанный контакт не существует"),
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Частичное обновление контакта",
        description="Обновляет контакт по указанному идентификатору.",
        responses={
            200: OpenApiResponse(
                response=ContactSerializer, description="Успешный ответ"
            ),
            401: OpenApiResponse(description="Необходима авторизация"),
            404: OpenApiResponse(description="Указанный контакт не существует"),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Удаление контакта",
        description="Удаляет контакт по указанному идентификатору.",
        responses={
            204: OpenApiResponse(response=None, description="Успешный ответ"),
            401: OpenApiResponse(description="Необходима авторизация"),
            404: OpenApiResponse(description="Указанный контакт не существует"),
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ProductsViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Создание продукта",
        description="Создает нового продукта.",
        responses={
            200: OpenApiResponse(
                response=ContactSerializer, description="Успешный запрос"
            ),
            400: OpenApiResponse(description="Некорректные данные"),
            401: OpenApiResponse(description="Необходима авторизация"),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Получение списка продуктов",
        description="Возвращает список всех продуктов.",
        responses={
            200: OpenApiResponse(
                response=ContactSerializer(many=True), description="Успешный ответ"
            ),
            401: OpenApiResponse(description="Необходима авторизация"),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Получение продукта",
        description="Возвращает продукт по указанному идентификатору.",
        responses={
            200: OpenApiResponse(
                response=ContactSerializer, description="Успешный ответ"
            ),
            401: OpenApiResponse(description="Необходима авторизация"),
            404: OpenApiResponse(description="Указанный продукт не существует"),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Обновление продукта",
        description="Обновляет продукт по указанному идентификатору.",
        responses={
            200: OpenApiResponse(
                response=ContactSerializer, description="Успешный ответ"
            ),
            401: OpenApiResponse(description="Необходима авторизация"),
            404: OpenApiResponse(description="Указанный продукт не существует"),
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Частичное обновление продукта",
        description="Обновляет продукт по указанному идентификатору.",
        responses={
            200: OpenApiResponse(
                response=ContactSerializer, description="Успешный ответ"
            ),
            401: OpenApiResponse(description="Необходима авторизация"),
            404: OpenApiResponse(description="Указанный контакт не существует"),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Удаление продукта",
        description="Удаляет продукт по указанному идентификатору.",
        responses={
            204: OpenApiResponse(response=None, description="Успешный ответ"),
            401: OpenApiResponse(description="Необходима авторизация"),
            404: OpenApiResponse(description="Указанный продукт не существует"),
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ChainLinkCreateAPIView(generics.CreateAPIView):
    serializer_class = ChainLinkSerializer

    @extend_schema(
        summary="Создание звеньев поставки",
        description="Создает новое звено поставки.",
        responses={
            200: OpenApiResponse(
                response=ContactSerializer, description="Успешный запрос"
            ),
            400: OpenApiResponse(description="Некорректные данные"),
            401: OpenApiResponse(description="Необходима авторизация"),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ChainLinkListAPIView(generics.ListAPIView):
    serializer_class = ChainLinkSerializer

    @extend_schema(
        summary="Получение списка звеньев цепочки поставки",
        description="Возвращает список всех звеньев.",
        responses={
            200: OpenApiResponse(
                response=ContactSerializer(many=True), description="Успешный ответ"
            ),
            401: OpenApiResponse(description="Необходима авторизация"),
        },
    )
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_queryset(self):
        country = self.request.query_params.get("country", None)
        if country:
            # Получение только тех данных, которые содержат переданную страну (поле и переданный параметр приводятся к нижнему регистру)
            return (
                ChainLink.objects.annotate(lowercase=Lower("contacts__country"))
                .filter(lowercase=country.lower())
                .order_by("id")
            )
        return ChainLink.objects.all().order_by("id")


class ChainLinkRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ChainLinkSerializer
    queryset = ChainLink.objects.all()

    @extend_schema(
        summary="Получение звена цепочки поставки",
        description="Возвращает звено посnfdrb по указанному идентификатору.",
        responses={
            200: OpenApiResponse(
                response=ContactSerializer, description="Успешный ответ"
            ),
            401: OpenApiResponse(description="Необходима авторизация"),
            404: OpenApiResponse(description="Указанное звено не существует"),
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ChainLinkUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ChainLinkUpdateSerializer
    queryset = ChainLink.objects.all()

    @extend_schema(
        summary="Обновление звена цепочки поставки",
        description="Обновляет звено цепочки поставки по указанному идентификатору.",
        responses={
            200: OpenApiResponse(
                response=ContactSerializer, description="Успешный ответ"
            ),
            401: OpenApiResponse(description="Необходима авторизация"),
            404: OpenApiResponse(description="Указанное звено не существует"),
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Частичное обновление звена цепочки поставки",
        description="Обновляет звено цепочки поставки по указанному идентификатору.",
        responses={
            200: OpenApiResponse(
                response=ContactSerializer, description="Успешный ответ"
            ),
            401: OpenApiResponse(description="Необходима авторизация"),
            404: OpenApiResponse(description="Указанное звено не существует"),
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class ChainLinkDeleteAPIView(generics.DestroyAPIView):
    queryset = ChainLink.objects.all()

    @extend_schema(
        summary="Удаление звена цепочки поставки",
        description="Удаляет звено цепочки поставки по указанному идентификатору.",
        responses={
            204: OpenApiResponse(response=None, description="Успешный ответ"),
            401: OpenApiResponse(description="Необходима авторизация"),
            404: OpenApiResponse(description="Указанный продукт не существует"),
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
