from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class DivineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DivineCategory
        fields = ['id', 'name']


class DivineSoftwareSerializer(serializers.ModelSerializer):
    category = DivineCategorySerializer()

    class Meta:
        model = DivineSoftware
        fields = ['id', 'name', 'description', 'image_url', 'price', 'quantity', 'category', 'has_key']


class DivineKeySerializer(serializers.ModelSerializer):
    software = DivineSoftwareSerializer()

    class Meta:
        model = DivineKey
        fields = ['id', 'key_code', 'software', 'is_used']


class DivineOrderDetailSerializer(serializers.ModelSerializer):
    key = DivineKeySerializer()

    class Meta:
        model = DivineOrderDetail
        fields = ['id', 'key', 'quantity']


class DivineOrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    order_details = DivineOrderDetailSerializer(many=True, read_only=True)

    class Meta:
        model = DivineOrder
        fields = ['id', 'user', 'order_date', 'status', 'order_details']


class DivineCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    software = DivineSoftwareSerializer()

    class Meta:
        model = DivineComment
        fields = ['id', 'user', 'software', 'text', 'created_at']


class CartItemSerializer(serializers.ModelSerializer):
    software = DivineSoftwareSerializer()

    class Meta:
        model = DivineCartItem
        fields = ['id', 'software', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = DivineCart
        fields = ['id', 'user', 'created_at', 'cart_items']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
