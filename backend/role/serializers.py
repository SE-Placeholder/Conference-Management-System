from django.contrib.auth.models import User
from rest_framework.fields import SerializerMethodField, JSONField
from rest_framework.serializers import ModelSerializer

from role.models import BidRole


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class BidSerializer(ModelSerializer):
    class Meta:
        model = BidRole
        fields = ['qualifier']
