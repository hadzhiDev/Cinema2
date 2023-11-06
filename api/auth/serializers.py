from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User 
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'last_login',
        )


class RegisterUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(validators=[validate_password])

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'username',
            'password'
        )
        extra_kwargs = {
            'last_name': {'required': True},
            'first_name': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user