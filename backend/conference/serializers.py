from rest_framework.fields import SerializerMethodField
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from conference.models import Conference
from role.models import Role, RoleTypes


class ConferenceSerializer(ModelSerializer):
    steering_committee = SerializerMethodField()
    papers = StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Conference
        fields = [
            'id',
            'title',
            'description',
            'deadline',
            'location',
            'date',
            'fee',
            'steering_committee',
            'papers'
        ]

    def create(self, validated_data):
        # print(self.context['request'].user)
        conference = super().create(validated_data)
        Role.objects.create(
            role=RoleTypes.STEERING_COMMITTEE,
            conference=conference,
            user=self.context['request'].user)
        return conference

    def get_steering_committee(self, conference):
        return map(lambda role: role.user.username,
                   Role.objects.filter(role=RoleTypes.STEERING_COMMITTEE, conference=conference))