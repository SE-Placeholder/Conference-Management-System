from rest_framework.serializers import ModelSerializer

from authentication.serializers import UserSerializer
from role.models import BidRole, ReviewerRole


class BidSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = BidRole
        fields = ['user', 'qualifier']


class ReviewSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ReviewerRole
        fields = ['user', 'qualifier', 'review']