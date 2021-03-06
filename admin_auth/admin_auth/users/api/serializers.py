from rest_framework import serializers
from ..models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=4, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)
    username = serializers.CharField(max_length=225, read_only=True)
    tokens = serializers.CharField(max_length=555, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, please specify correct credentials')
        if not user.is_active:
            raise AuthenticationFailed('Your account is inactive')
        if not user.is_verified:
            raise AuthenticationFailed('Please verify your email')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }


class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']

        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
