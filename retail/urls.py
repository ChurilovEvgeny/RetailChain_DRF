from django.urls import path
from rest_framework.routers import DefaultRouter

from retail.apps import RetailConfig
from retail.views import (
    ChainCreateAPIView,
    ChainListAPIView,
    ChainRetrieveAPIView,
    ContactsViewSet,
    ProductsViewSet,
    ChainUpdateAPIView,
    ChainDeleteAPIView,
)

app_name = RetailConfig.name

contactRouter = DefaultRouter()
contactRouter.register(r"contacts", ContactsViewSet, basename="contacts")

productRouter = DefaultRouter()
productRouter.register(r"products", ProductsViewSet, basename="products")

urlpatterns = (
    [
        path(
            "chain/create/",
            ChainCreateAPIView.as_view(),
            name="chain-create",
        ),
        path(
            "chain/list/",
            ChainListAPIView.as_view(),
            name="chain-list",
        ),
        path(
            "chain/<int:pk>/",
            ChainRetrieveAPIView.as_view(),
            name="chain-retrieve",
        ),
        path(
            "chain/update/<int:pk>/",
            ChainUpdateAPIView.as_view(),
            name="chain-update",
        ),
        path(
            "chain/delete/<int:pk>/",
            ChainDeleteAPIView.as_view(),
            name="chain-delete",
        ),
    ]
    + contactRouter.urls
    + productRouter.urls
)
