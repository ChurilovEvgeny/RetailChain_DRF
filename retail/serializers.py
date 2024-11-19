from rest_framework import serializers

from retail.models import Chain, Contact, Product


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chain
        fields = "__all__"
        # read_only_fields = (
        #     "id",
        #     "created_at",
        #     "title",
        #     "is_confirmed",
        #     "token",
        # )
