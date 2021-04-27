from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import UserSerializer


class StateInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "authenticated": True,
            "user": UserSerializer(request.user).data
            # , "user_list": UserSerializer(User.objects.all(), many=True).data
        }, status=status.HTTP_200_OK)
