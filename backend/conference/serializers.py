from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField, JSONField
from rest_framework.serializers import ModelSerializer, Serializer

from api.utils import get_user, try_except
from conference.models import Conference
from proposal.models import Proposal
from proposal.serializers import ProposalSerializer
from role.models import SteeringCommitteeRole, ListenerRole
from authentication.serializers import UserSerializer


# TODO: refactor
class ConferenceSerializer(ModelSerializer):
    steering_committee = JSONField(binary=True, write_only=True, required=False)
    proposals = SerializerMethodField()

    class Meta:
        model = Conference
        fields = ['id', 'title', 'description', 'location', 'date', 'fee',
                  'abstract_deadline', 'proposal_deadline', 'bidding_deadline',
                  'steering_committee', 'proposals']

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
            SteeringCommitteeRole.objects.create(user=user, conference=conference)

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
    def get_proposals(conference):
        proposals = ProposalSerializer(Proposal.objects.filter(conference=conference), many=True)
        return proposals.data


class JoinConferenceSerializer(Serializer):
    def create(self, validated_data):
        user = self.context['user']
        conference = try_except(
            lambda: Conference.objects.get(id=self.context['id']),
            ValidationError({'detail': 'Conference not found.'}))

        if ListenerRole.objects.filter(user=user, conference=conference).exists():
            raise ValidationError({'detail': 'Already registered for this conference.'})

        return ListenerRole.objects.create(user=user, conference=conference)