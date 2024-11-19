from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from retail.models import Chain, Contact, Product
from retail.serializers import ChainSerializer, ContactSerializer, ProductSerializer


class ContactsViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ProductsViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ChainCreateAPIView(generics.CreateAPIView):
    """Создание документа"""

    serializer_class = ChainSerializer
    # permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     obj = serializer.save(owner=self.request.user)
    #     obj.title = str(self.request.FILES.get("file"))
    #     obj.token = secrets.token_hex(32)
    #     obj.save()


class ChainListAPIView(generics.ListAPIView):
    """Просмотр списка своих документов"""

    serializer_class = ChainSerializer
    # permission_classes = [IsAuthenticated, IsOwner]
    queryset = Chain.objects.all().order_by("id")

    # def get_queryset(self):
    #     # возврат кверисета для текущего пользователя
    #     return self.queryset.filter(owner=self.request.user)


class ChainRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр документа"""

    serializer_class = ChainSerializer
    queryset = Chain.objects.all()
    # permission_classes = [IsAuthenticated, IsOwner]


class ChainUpdateAPIView(generics.UpdateAPIView):
    """Изменение изображения"""

    serializer_class = ChainSerializer
    queryset = Chain.objects.all()
    # permission_classes = [IsAuthenticated, IsOwner]


    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class ChainDeleteAPIView(generics.DestroyAPIView):
    """Удаление изображения"""

    queryset = Chain.objects.all()
    # permission_classes = [IsAuthenticated, IsOwner]


    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


