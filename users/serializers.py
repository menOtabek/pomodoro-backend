from rest_framework import serializers
from .models import OTP

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class OTPKeySerializer(serializers.Serializer):
    otp_key = serializers.CharField()
    email = serializers.EmailField()

class VerifyOTPSerializer(serializers.Serializer):
    code = serializers.CharField()
    otp_key = serializers.CharField()
    email = serializers.EmailField()

class OTPModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ('otp_key', 'code', 'email', 'created_at')
