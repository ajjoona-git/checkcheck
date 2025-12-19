from rest_framework import serializers
from .models import Product, ProductOption

class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = '__all__'