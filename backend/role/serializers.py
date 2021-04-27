from rest_framework.serializers import ModelSerializer

from authentication.serializers import UserSerializer
from role.models import BidRole


class BidSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = BidRole
        fields = ['user', 'qualifier']
