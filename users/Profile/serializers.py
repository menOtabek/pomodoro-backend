from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from users.models import OTP

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    otp_key = serializers.CharField(write_only=True, required=True)
    picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'picture', 'username', 'otp_key')

    def create(self, validated_data):
        otp_key = validated_data.pop('otp_key')
        if not OTP.objects.filter(otp_key=otp_key, email=validated_data.get('email'), is_verified=True).exists():
            raise serializers.ValidationError('OTP key not verified or email is invalid')

        OTP.objects.filter(otp_key=otp_key, email=validated_data.get('email'), is_verified=True).delete()

        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data.get('password'),
            username=validated_data.get('username'),
            picture=validated_data.get('picture'),
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data.get('email'), password=data.get('password'))
        if not user:
            raise AuthenticationFailed("Invalid email or password")
        data['user'] = user
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField()
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'picture']
        read_only_fields = ['id', 'email']


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()