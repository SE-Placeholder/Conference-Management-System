from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField, ListField, JSONField
from rest_framework.serializers import ModelSerializer

from api.utils import get_user
from conference.models import Conference
from paper.models import Paper
from paper.serializers import PaperSerializer
from role.models import SteeringCommitteeRole
from role.serializers import UserSerializer


class ConferenceSerializer(ModelSerializer):
    steering_committee = JSONField(binary=True, write_only=True, required=False)
    papers = SerializerMethodField()

    class Meta:
        model = Conference
        fields = ['id', 'title', 'description', 'deadline', 'location', 'date', 'fee', 'steering_committee', 'papers']

    def create(self, validated_data):
        steering_committee = [self.context['request'].user]
        errors = []

        for user_id in list(set(validated_data.pop('steering_committee', []))):
            user = get_user(user_id)
            if user:
                steering_committee.append(user)
            else:
                errors.append(f'user {user_id} not found.')

        if errors:
            raise ValidationError({'steering_committee': errors})

        conference = super().create(validated_data)

        for user in steering_committee:
            SteeringCommitteeRole.objects.create(
                user=user,
                conference=conference)

        return conference

    def update(self, instance, validated_data):
        steering_committee = []
        errors = []

        for user_id in list(set(validated_data.pop('steering_committee', []))):
            user = get_user(user_id)
            if user:
                steering_committee.append(user)
            else:
                errors.append(f'user {user_id} not found.')

        if errors:
            raise ValidationError({'steering_committee': errors})

        conference = super().update(instance, validated_data)

        if steering_committee:
            for role in SteeringCommitteeRole.objects.filter(conference=conference):
                role.delete()

        for user in steering_committee:
            SteeringCommitteeRole.objects.create(user=user, conference=conference)

        return conference

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['steering_committee'] = UserSerializer(
            map(lambda role: role.user, SteeringCommitteeRole.objects.filter(conference=instance)),
            many=True).data
        return data

    @staticmethod
    def get_papers(conference):
        papers = PaperSerializer(
            Paper.objects.filter(conference=conference),
            many=True)
        return papers.data
