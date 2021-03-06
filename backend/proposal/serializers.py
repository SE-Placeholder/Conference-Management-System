from rest_framework.exceptions import ValidationError
from rest_framework.fields import JSONField, SerializerMethodField, ListField, ChoiceField, CharField
from rest_framework.serializers import ModelSerializer, Serializer

from api.utils import get_user, try_except
from authentication.serializers import UserSerializer
from proposal.models import Proposal
from role.models import AuthorRole, ReviewerRole, SteeringCommitteeRole, BidRole
from role.serializers import BidSerializer, ReviewSerializer


class ProposalSerializer(ModelSerializer):
    authors = JSONField(binary=True, write_only=True, required=False)
    bids = SerializerMethodField()
    reviews = SerializerMethodField()

    class Meta:
        model = Proposal
        fields = ['id', 'title', 'conference', 'topics', 'keywords', 'abstract', 'paper', 'bids', 'reviews', 'authors']

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

        # for bidder in SteeringCommitteeRole.objects.filter(conference=proposal.conference):
        #     BidRole.objects.create(user=bidder.user, proposal=proposal).save()

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

        # for bidder in SteeringCommitteeRole.objects.filter(conference=proposal.conference):
        #     BidRole.objects.create(user=bidder.user, proposal=proposal).save()

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
    def get_reviews(proposal):
        return ReviewSerializer(
            ReviewerRole.objects.filter(proposal=proposal),
            many=True
        ).data


class BidProposalSerializer(Serializer):
    qualifier = ChoiceField(choices=BidRole.qualifier_choices)

    def create(self, validated_data):
        user = self.context['user']
        proposal = self.context['proposal']

        bid = BidRole.objects.filter(user=user, proposal=proposal)
        if bid.exists():
            bid.delete()

        return BidRole.objects.create(user=user, proposal=proposal, qualifier=validated_data['qualifier'])


class AssignReviewersSerializer(Serializer):
    reviewers = ListField()

    def create(self, validated_data):
        proposal = self.context['proposal']
        reviewers = []
        errors = []

        for reviewer in validated_data['reviewers']:
            user = get_user(reviewer)
            if user:
                reviewers.append(ReviewerRole(
                    user=user,
                    proposal=proposal))
            else:
                errors.append(f'user {reviewer} not found.')

        if errors:
            raise ValidationError({'error': errors})

        for role in ReviewerRole.objects.filter(proposal=proposal):
            role.delete()

        for reviewer in reviewers:
            reviewer.save()

        for bid in BidRole.objects.filter(proposal=proposal):
            bid.delete()

        return reviewers


class AddReviewSerializer(Serializer):
    qualifier = ChoiceField(choices=ReviewerRole.qualifier_choices)
    review = CharField(max_length=1024)

    def create(self, validated_data):
        user = self.context['user']
        proposal = self.context['proposal']

        review = ReviewerRole.objects.filter(user=user, proposal=proposal)
        if review.exists():
            review.delete()

        return ReviewerRole.objects.create(
            user=user,
            proposal=proposal,
            qualifier=validated_data['qualifier'],
            review=validated_data['review'])
