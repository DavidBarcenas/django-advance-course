from django.contrib.auth import authenticate, password_validation
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator

from cride.users.models import User, Profile


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer"""

    class Meta:
        """Meta class"""

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number'
        )


class UserLoginSerializer(serializers.Serializer):
    """User Login serializer
    
    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials"""

        user = authenticate(
            username = data['email'], 
            password = data['password']
        )

        if not user:
            raise serializers.ValidationError('Invalid credentials.')

        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet :(')

        self.context['user'] = user

        return data

    def create(self, data):
        """Generate or retrieve new token"""

        token, created = Token.objects.get_or_create(user=self.context['user'])

        return self.context['user'], token.key


class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer
    
    Handle sign up data validation and user/profile creation.
    """

    email = serializers.EmailField(
        validators = [UniqueValidator(queryset=User.objects.all())]
    )

    username = serializers.CharField(
        min_length = 4,
        max_length = 20,
        validators = [UniqueValidator(queryset=User.objects.all())]
    )

    phone_regex = RegexValidator(
        regex = r'\+?1?\d{9,15}$',
        message = (
            'Phone number must be entered in the format: 5588996658. '
            'Up to 15 digits allowed.'
        )
    )

    phone_number = serializers.CharField(
        validators = [phone_regex],
        max_length = 17, 
    )

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data):
        """Verify password match."""

        password = data['password']
        password_conf = data['password_confirmation']

        if password != password_conf:
            raise serializers.ValidationError('Passwords does not match.')

        password_validation.validate_password(password)

        return data

    def create(self, data):
        """Handle user and profile creation."""

        data.pop('password_confirmation')

        user = User.objects.create_user(**data, is_verified=False)
        Profile.objects.create(user=user)

        return user

         