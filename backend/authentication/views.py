from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class IsAuthenticatedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"authenticated": True}, status=status.HTTP_200_OK)


# class IsAuthenticatedView(APIView):
#     def get(self, request):
#         if isinstance(request.user, AnonymousUser):
#             return Response({"authenticated": False}, status=status.HTTP_200_OK)
#         else:
#             return Response({"authenticated": True}, status=status.HTTP_200_OK)
#