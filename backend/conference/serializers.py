from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField, JSONField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, Serializer

from api.utils import get_user
from conference.models import Conference, Section
from proposal.models import Proposal
from proposal.serializers import ProposalSerializer
from role.models import SteeringCommitteeRole, ListenerRole
from authentication.serializers import UserSerializer
from role.serializers import ListenerSerializer


class SectionSerializer(ModelSerializer):
    proposals = SerializerMethodField()

    class Meta:
        model = Section
        fields = ['id', 'title', 'start', 'end', 'conference', 'proposals']
        depth = 1

    def get_proposals(self, section):
        return ProposalSerializer(
            Proposal.objects.filter(conference=section.conference),
            many=True).data


class ConferenceSerializer(ModelSerializer):
    steering_committee = JSONField(binary=True, write_only=True, required=False)
    sections = JSONField(binary=True, write_only=True, required=False)
    listeners = SerializerMethodField()
    proposals = SerializerMethodField()

    class Meta:
        model = Conference
        fields = ['id', 'title', 'description', 'location', 'date', 'fee',
                  'abstract_deadline', 'proposal_deadline', 'bidding_deadline',
                  'steering_committee', 'sections', 'listeners', 'proposals']

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

        for section in Section.objects.filter(conference=instance):
            section.delete()

        print(validated_data.get('sections', []))

        for section in validated_data.pop('sections', []):
            Section.objects.create(
                title=section["title"],
                start=section["start"],
                end=section["end"],
                conference=instance)

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
        data['sections'] = SectionSerializer(
            Section.objects.filter(conference=instance),
            many=True).data
        return data

    @staticmethod
    def get_proposals(conference):
        return ProposalSerializer(
            Proposal.objects.filter(conference=conference),
            many=True
        ).data

    @staticmethod
    def get_listeners(conference):
        return ListenerSerializer(
            ListenerRole.objects.filter(conference=conference),
            many=True
        ).data


class JoinConferenceSerializer(Serializer):
    def create(self, validated_data):
        user = self.context['user']
        conference = self.context['conference']

        if ListenerRole.objects.filter(user=user, conference=conference).exists():
            raise ValidationError({'detail': 'Already registered for this conference.'})

        return ListenerRole.objects.create(user=user, conference=conference)


class JoinSectionSerializer(Serializer):
    section = PrimaryKeyRelatedField(queryset=Section.objects.all(), write_only=True)

    def create(self, validated_data):
        user = self.context['user']
        conference = self.context['conference']

        if not ListenerRole.objects.filter(user=user, conference=conference).exists():
            raise ValidationError({'detail': 'Not registered for this conference.'})

        sections = ListenerRole.objects.get(user=user, conference=conference).sections

        if sections.filter(id=validated_data['section'].id).exists():
            raise ValidationError({'detail': 'Already joined this section.'})

        sections.add(validated_data['section'])
        raise ValidationError({'detail': 'Successfully joined section.'})