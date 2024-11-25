from rest_framework import serializers

from retail.models import ChainLink, Contact, Product


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ChainLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChainLink
        fields = "__all__"


class ChainLinkUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChainLink
        fields = "__all__"
        read_only_fields = ("dept",)
