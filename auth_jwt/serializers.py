from rest_framework import serializers
from .models import Auth, Token


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('id', 'user', 'token', 'deviceID')


class BaseSerializer(serializers.ModelSerializer):
    loginID = serializers.CharField(min_length=5)
    password = serializers.CharField(min_length=8, write_only=True)
    # appID = serializers.CharField(required=False)

    class Meta:
        model = Auth
        fields = ('id', 'loginID', 'password', 'deviceID', 'is_active')


class LoginSerializer(serializers.Serializer):
    loginID = serializers.CharField(min_length=5)
    password = serializers.CharField(min_length=8, write_only=True)
    appID = serializers.CharField()
    deviceID = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    loginID = serializers.CharField(min_length=5)
    appID = serializers.CharField()
    old_password = serializers.CharField(min_length=8, write_only=True)
    new_password = serializers.CharField(min_length=8, write_only=True)


class SetPasswordSerializer(serializers.Serializer):
    loginID = serializers.CharField(min_length=5)
    password = serializers.CharField(min_length=8, write_only=True)
    appID = serializers.CharField()


class DeactiveSerializer(serializers.Serializer):
    loginID = serializers.CharField(min_length=5)
    appID = serializers.CharField()
