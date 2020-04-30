from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Product, Order, OrderProduct


class ProductsSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(read_only=True, source='creator.username')
    published = serializers.IntegerField(read_only=True, source='published_date.create.timestamp')

    class Meta:
        model = Product
        fields = ('id', 'creator', 'name', 'description', 'price', 'imageUrl', 'published', 'discount')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "username", "password")


class OrderSerializer(serializers.ModelSerializer):
    # products = serializers.PrimaryKeyRelatedField(OrderProduct)

    class Meta:
        model = Order
        fields = ('id', 'products')


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('_all_',)
