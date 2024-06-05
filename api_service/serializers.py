from rest_framework import serializers, fields, filters
from .models import *
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'name', 'gender')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ( 'name', 'gender',)

class UpdatePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ( 'password',)

    def update(self, instance, validated_data):
    
        instance.set_password(validated_data['password'])
        instance.save()
        return instance   

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name']


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserListSerializer(read_only=True)
    to_user = UserListSerializer(read_only=True)
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'timestamp']