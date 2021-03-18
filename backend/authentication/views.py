from django.contrib.auth.models import update_last_login
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status


class TestView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response('boi', status=status.HTTP_200_OK)


class RegisterView(GenericAPIView):
    permission_classes = ()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenViewBase):
    permission_classes = ()
    serializer_class = TokenObtainPairSerializer


# class TokenRefreshView(TokenViewBase):
#     serializer_class = TokenRefreshSerializer


# TODO: refactor this
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except KeyError as error:
            print('what')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except TokenError as error:
            print('what2')
            return Response(status=status.HTTP_400_BAD_REQUEST)
