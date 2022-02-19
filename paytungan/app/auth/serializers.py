from django.contrib.auth.models import User, Group
from rest_framework import serializers


class GetUserRequest(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    username = serializers.CharField()
    email = serializers.CharField()


class GetUserResponse(serializers.Serializer):
    data = UserSerializer()
