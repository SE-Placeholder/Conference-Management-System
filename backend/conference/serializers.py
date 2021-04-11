from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from conference.models import Conference
from role.models import Role


class ConferenceSerializer(ModelSerializer):
    steering_committee = SerializerMethodField()

    class Meta:
        model = Conference
        fields = ['id', 'title', 'description', 'deadline', 'steering_committee']

    def create(self, validated_data):
        print(self.context['request'].user)
        conference = super().create(validated_data)
        role = Role(role='steering committee', conference=conference, user=self.context['request'].user)
        role.save()
        return conference

    def get_steering_committee(self, conference):
        return map(lambda role: role.user.username,
                   Role.objects.filter(role='steering committee', conference=conference))