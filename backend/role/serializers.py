from rest_framework.serializers import ModelSerializer

from authentication.serializers import UserSerializer
from role.models import BidRole, ReviewerRole, ListenerRole


class ListenerSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ListenerRole
        fields = ['user', 'sections']


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