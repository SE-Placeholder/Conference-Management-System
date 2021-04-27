from rest_framework.serializers import ModelSerializer

from role.models import BidRole


class BidSerializer(ModelSerializer):
    class Meta:
        model = BidRole
        fields = ['qualifier']
