from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenViewBase
from .serializers import UserSerializer, TokenDisableSerializer


class PingView(GenericAPIView):
    permission_classes = ()

    def get(self, request):
        return Response('pong', status=status.HTTP_200_OK)


class RestrictedPingView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return Response('pong', status=status.HTTP_200_OK)


class RegisterView(GenericAPIView):
    permission_classes = ()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtainView(TokenViewBase):
    permission_classes = ()
    serializer_class = TokenObtainPairSerializer


class TokenRefreshView(TokenViewBase):
    permission_classes = ()
    serializer_class = TokenRefreshSerializer


class TokenDisableView(TokenViewBase):
    permission_classes = ()
    serializer_class = TokenDisableSerializer
