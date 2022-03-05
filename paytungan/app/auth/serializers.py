from django.contrib.auth.models import User, Group
from rest_framework import serializers


class GetUserRequest(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    firebase_uid = serializers.CharField()
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    phone_number = serializers.CharField()
    profil_image = serializers.CharField(required=False)
    is_onboarding = serializers.BooleanField(default=False)


class GetUserResponse(serializers.Serializer):
    data = UserSerializer()


class CreateUserRequest(serializers.Serializer):
    firebase_uid = serializers.CharField()
    phone_number = serializers.CharField()


class CreateUserResponse(serializers.Serializer):
    data = UserSerializer()


class LoginRequest(serializers.Serializer):
    token = serializers.CharField()


class LoginResponse(serializers.Serializer):
    user = UserSerializer()
