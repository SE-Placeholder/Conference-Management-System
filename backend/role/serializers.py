from django.contrib.auth.models import User
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from conference.models import Conference
from conference.serializers import ConferenceSerializer
from paper.serializers import PaperSerializer
from role.models import Role


class RoleSerializer(ModelSerializer):
    conference = ConferenceSerializer(read_only=True)
    paper = PaperSerializer(read_only=True)

    class Meta:
        model = Role
        fields = ['role', 'conference', 'paper']

    # TODO: handle this in a different way
    def to_representation(self, instance):
        data = super().to_representation(instance)
        items = []
        for key, value in data.items():
            print(key, value)
            if value is None:
                items.append(key)
        for item in items:
            data.pop(item)
        return data


class UserSerializer(ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'roles']
