from rest_framework.exceptions import ValidationError
from rest_framework.fields import JSONField, SerializerMethodField, ListField
from rest_framework.serializers import ModelSerializer, Serializer

from api.utils import get_user
from proposal.models import Proposal, Bid
from role.models import AuthorRole, ReviewerRole
from role.serializers import UserSerializer


# TODO: handle qualifier representation on model
class BidSerializer(ModelSerializer):
    user = SerializerMethodField()
    qualifier = SerializerMethodField()

    class Meta:
        model = Bid
        fields = ['user', 'qualifier']

    @staticmethod
    def get_user(bid):
        return UserSerializer(bid.user).data

    @staticmethod
    def get_qualifier(bid):
        qualifiers = {
            -1: 'negative',
            0: 'neutral',
            1: 'positive'
        }
        return bid.qualifier
        # qualifiers[bid.qualifier]


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
        return BidSerializer(Bid.objects.filter(proposal=proposal), many=True).data

    @staticmethod
    def get_reviewers(proposal):
        return UserSerializer(
            map(lambda reviewer: reviewer.user, ReviewerRole.objects.filter(proposal=proposal)),
            many=True
        ).data


class AssignReviewersSerializer(Serializer):
    reviewers = ListField()
