from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField, JSONField
from rest_framework.serializers import ModelSerializer

from api.utils import get_user
from conference.models import Conference
from proposal.models import Proposal
from proposal.serializers import ProposalSerializer
from role.models import SteeringCommitteeRole
from authentication.serializers import UserSerializer


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

    # @staticmethod
    # def get_needs_reviewer_repartition(conference):
    #     print(timezone.now())
    #     print(conference.bidding_deadline)
    #     if timezone.now() < conference.bidding_deadline:
    #         return False
    #
    #     proposals = Proposal.objects.filter(conference=conference)
    #     if ReviewerRole.objects.filter(**{'proposal__in': proposals}).exists():
    #         return False
    #
    #     return True
