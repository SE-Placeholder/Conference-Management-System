from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from role.serializers import UserSerializer


class StateInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "authenticated": True,
            "username": request.user.username,
            "user_id": request.user.id,
            "user_list": UserSerializer(User.objects.all(), many=True).data
        }, status=status.HTTP_200_OK)
