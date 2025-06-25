from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema

from .models import OTP, User
from .serializers import EmailSerializer, VerifyOTPSerializer, OTPModelSerializer, OTPKeySerializer
from .utils import generate_code, generate_key


class OTPViewSet(ModelViewSet):
    queryset = OTP.objects.all()
    serializer_class = OTPModelSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        request=EmailSerializer,
        responses=OTPKeySerializer,
        description="Send email",
        summary="Send email",
        tags=["OTP"],
    )
    @action(detail=False, methods=['post'], url_path='request')
    def request_otp(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # code = generate_code()
        otp_key = generate_key()

        otp = OTP.objects.create(email=email, code=102030, otp_key=otp_key)

        print(f"EMAIL: {email}, OTP_CODE: {102030}")

        return Response(data=OTPKeySerializer(otp).data, status=status.HTTP_200_OK)

    @extend_schema(
        request=VerifyOTPSerializer,
        responses={200: dict, 400: dict},
        description="Send otp code and otp key to verify email.",
        summary="Verify email",
        tags=["OTP"],
    )
    @action(detail=False, methods=['post'], url_path='verify')
    def verify_otp(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')
        otp_key = serializer.validated_data.get('otp_key')
        email = serializer.validated_data.get('email')

        valid_time = timezone.now() - timedelta(minutes=5)

        otp = OTP.objects.filter(
            code=code,
            otp_key=otp_key,
            email=email,
            created_at__gte=valid_time,
            is_verified=False
        ).last()

        if not otp:
            return Response(data='Invalid or expired OTP', status=status.HTTP_400_BAD_REQUEST)

        otp.is_verified = True
        otp.save()

        return Response(data='OTP verified', status=status.HTTP_200_OK)
