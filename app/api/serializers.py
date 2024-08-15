from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from .models import Inventory, Barracks

User = get_user_model()


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['items', 'capacity']


class BarracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barracks
        fields = ['troops', 'max_level']


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password')


class CustomUserSerializer(UserSerializer):
    inventory = InventorySerializer(read_only=True)
    barracks = BarracksSerializer(read_only=True)

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'inventory', 'barracks')
