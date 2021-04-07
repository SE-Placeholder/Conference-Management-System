from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, RetrieveAPIView

from role.serializers import UserSerializer


class ListUsersView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GetUserView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
