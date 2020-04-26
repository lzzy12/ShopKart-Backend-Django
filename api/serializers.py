from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Product


class ProductsSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(read_only=True, source='creator.username')

    class Meta:
        model = Product
        fields = ['id', 'creator', 'name', 'description', 'price', 'imageUrl']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "username", "password")
