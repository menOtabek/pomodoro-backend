from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer, ChangePasswordSerializer, TokenSerializer, \
    UserProfileSerializer, RefreshTokenSerializer

User = get_user_model()


class RegisterViewSet(ViewSet):
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request=RegisterSerializer,
        responses=TokenSerializer(),
        tags=['Auth'],
        summary="Register new user",
        description="Registers a new user and returns JWT refresh and access tokens",
    )
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(data={
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class AuthViewSet(ViewSet):
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action == 'change_password':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @extend_schema(
        request=LoginSerializer,
        responses=TokenSerializer(),
        tags=['Auth'],
        summary="Login user",
        description="Authenticates a user using email and password. Returns JWT tokens"
    )
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        refresh = RefreshToken.for_user(user)
        return Response(data={
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiResponse(description="'Password updated successfully"),
            400: OpenApiResponse(description="Old password incorrect or validation failed"),
        },
        tags=['Auth'],
        summary="Change user password",
        description="Allows an authenticated user to change their password"
    )
    def change_password(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not user.check_password(serializer.validated_data['old_password']):
            raise ValidationError('Old password incorrect or validation failed')
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response(data='Password updated successfully', status=status.HTTP_200_OK)


class ProfileViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: UserProfileSerializer},
        tags=['User'],
        summary="Users profile",
        description="Profile of users"
    )
    def list_profile(self, request):
        users = User.objects.filter(is_active=True)
        serializer = UserProfileSerializer(users, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UpdateProfileViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        responses={200: UserProfileSerializer},
        tags=['User'],
        summary="Get profile",
        description="Authenticated user returns own profile data"
    )
    def profile(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=UserProfileSerializer,
        responses={200: UserProfileSerializer},
        tags=['User'],
        summary="Update profile",
        description="Authenticated user updates their profile (first_name, last_name)"
    )
    def update_profile(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # @extend_schema(
    #     request=RefreshTokenSerializer,
    #     responses={200: TokenSerializer},
    #     tags=['Auth'],
    #     summary="Refresh token",
    #     description="Refresh users token"
    # )
    # def refresh_token(self, request):
    #     serializer = RefreshTokenSerializer(request.data)
    #     serializer.is_valid(raise_exception=True)
    #     pass