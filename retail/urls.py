from django.urls import path
from rest_framework.routers import DefaultRouter

from retail.apps import RetailConfig
from retail.views import (
    ChainLinkCreateAPIView,
    ChainLinkListAPIView,
    ChainLinkRetrieveAPIView,
    ContactsViewSet,
    ProductsViewSet,
    ChainLinkUpdateAPIView,
    ChainLinkDeleteAPIView,
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
            ChainLinkCreateAPIView.as_view(),
            name="chain-create",
        ),
        path(
            "chain/list/",
            ChainLinkListAPIView.as_view(),
            name="chain-list",
        ),
        path(
            "chain/<int:pk>/",
            ChainLinkRetrieveAPIView.as_view(),
            name="chain-retrieve",
        ),
        path(
            "chain/update/<int:pk>/",
            ChainLinkUpdateAPIView.as_view(),
            name="chain-update",
        ),
        path(
            "chain/delete/<int:pk>/",
            ChainLinkDeleteAPIView.as_view(),
            name="chain-delete",
        ),
    ]
    + contactRouter.urls
    + productRouter.urls
)
