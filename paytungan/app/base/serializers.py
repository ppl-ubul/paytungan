from rest_framework import serializers


class BaseHeaderRequest(serializers.Serializer):
    x_request_id = serializers.CharField(required=False)


class AuthHeaderRequest(BaseHeaderRequest):
    Authentication = serializers.CharField()
