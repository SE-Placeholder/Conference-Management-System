from rest_framework.exceptions import ValidationError
from rest_framework.fields import JSONField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from api.utils import get_user
from proposal.models import Proposal
from role.models import AuthorRole, ReviewerRole, SteeringCommitteeRole, BidRole
from role.serializers import UserSerializer, BidSerializer


class ProposalSerializer(ModelSerializer):
    authors = JSONField(binary=True, write_only=True, required=False)
    bids = SerializerMethodField()
    reviewers = SerializerMethodField()

    class Meta:
        model = Proposal
        fields = ['id', 'title', 'conference', 'topics', 'keywords', 'abstract', 'paper', 'bids', 'reviewers', 'authors']

    def create(self, validated_data):
        authors = [self.context['request'].user]
        errors = []

        for user_id in list(set(validated_data.pop('authors', []))):
            user = get_user(user_id)
            if user:
                authors.append(user)
            else:
                errors.append(f'user {user_id} not found.')

        if errors:
            raise ValidationError({'authors': errors})

        proposal = super().create(validated_data)

        for user in authors:
            AuthorRole.objects.create(user=user, proposal=proposal)

        for bidder in SteeringCommitteeRole.objects.filter(conference=proposal.conference):
            BidRole.objects.create(user=bidder.user, proposal=proposal).save()

        return proposal

    def update(self, instance, validated_data):
        authors = []
        errors = []

        for user_id in list(set(validated_data.pop('authors', []))):
            user = get_user(user_id)
            if user:
                authors.append(user)
            else:
                errors.append(f'user {user_id} not found.')

        if errors:
            raise ValidationError({'authors': errors})

        proposal = super().update(instance, validated_data)

        if authors:
            for role in AuthorRole.objects.filter(proposal=proposal):
                role.delete()

        for user in authors:
            AuthorRole.objects.create(user=user, proposal=proposal)

        return proposal

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['authors'] = UserSerializer(
            map(lambda role: role.user, AuthorRole.objects.filter(proposal=instance)),
            many=True).data
        return representation

    @staticmethod
    def get_bids(proposal):
        return BidSerializer(BidRole.objects.filter(proposal=proposal), many=True).data

    @staticmethod
    def get_reviewers(proposal):
        return UserSerializer(
            map(lambda reviewer: reviewer.user, ReviewerRole.objects.filter(proposal=proposal)),
            many=True
        ).data
