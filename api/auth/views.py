from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth import authenticate

from api.auth.serializers import LoginSerializer, UserSerializer, RegisterUserSerializer


class LoginGenericAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user:
            token = Token.objects.get_or_create(user=user)[0]
            user_serializer = UserSerializer(instance=user, context={'request': request})
            return Response({
                **user_serializer.data,
                'token': token.key
            })
        return Response({
            'message': 'The user not foun or invalid password',},
            status=status.HTTP_400_BAD_REQUEST)


class RegisterGenericAPIView(GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request):
        serilalizer = self.get_serializer(data=request.data)
        serilalizer.is_valid(raise_exception=True)
        user = serilalizer.save()
        token = Token.objects.get_or_create(user=user)[0]
        user_serializer = UserSerializer(instance=user, context={'request': request})
        return Response({
            **user_serializer.data,
            'token': token.key,
        })