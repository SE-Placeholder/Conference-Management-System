from django.core import serializers
from django.db import IntegrityError
from rest_framework import status
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from proposal.models import Proposal
from proposal.serializers import ProposalSerializer
from role.models import AuthorRole, SteeringCommitteeRole, BidRole

# create proposal: allow authenticated users
# list proposals: allow any
# update proposal: allow only users with author role for that proposal
# retrieve proposal: allow any
from role.serializers import BidSerializer


class ProposalPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not bool(request.user and request.user.is_authenticated):
            return False
        return AuthorRole.objects.filter(user=request.user, proposal=obj).exists()


class ProposalBidPermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(request.user and
                    request.user.is_authenticated and
                    SteeringCommitteeRole.objects.filter(user=request.user, conference=obj.conference).exists()
                    )


# TODO?: Modify the 2 classes into one
class BidPermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(request.user and
                    request.user.is_authenticated and
                    SteeringCommitteeRole.objects.filter(user=request.user, conference=obj.proposal.conference).exists()
                    )


class ProposalViewSet(ModelViewSet):
    serializer_class = ProposalSerializer
    permission_classes = [ProposalPermissions, ProposalBidPermissions]
    lookup_field = 'id'

    def get_queryset(self):
        return Proposal.objects.filter(conference__committee__user=self.request.user)


class BidProposalView(ModelViewSet):
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated, BidPermissions]

    def get_queryset(self):
        return BidRole.objects.filter(proposal=self.kwargs['id'])

    def retrieve(self, request, *args, **kwargs):
        data = self.get_queryset().all().values()

        if len(data) == 0:
            return Response({}, status=status.HTTP_200_OK)

        self.kwargs['pk'] = data[0]['id']
        return super().retrieve(request, *args, *kwargs)

    def partial_update(self, request, *args, **kwargs):
        if len(self.get_queryset().all().values()) == 0:
            return self.create(request)
        self.kwargs['pk'] = self.get_queryset().all().values()[0]['id']
        return super().partial_update(request, *args, *kwargs)

    def create(self, request, id=-1):
        try:
            new_bid = BidRole(proposal_id=id, user=request.user, qualifier=request.data['qualifier']).save()
        except IntegrityError as error:
            return self.partial_update(request)
        return Response(new_bid, status=status.HTTP_201_CREATED)


# TODO: change permission class, allow only steering committee members
# TODO: error checking and move everything into serializer
class AssignReviewersView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, id):
        serializer = AssignReviewersSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # TODO: check
        proposal = Proposal.objects.get(id=id)

        reviewers = []
        errors = []

        for reviewer in serializer.validated_data['reviewers']:
            user = get_user(reviewer)
            if user:
                reviewers.append(ReviewerRole(
                    user=user,
                    proposal=proposal))
            else:
                errors.append(f'user {reviewer} not found.')

        if errors:
            return Response({'error': errors}, status=status.HTTP_400_BAD_REQUEST)

        for role in ReviewerRole.objects.filter(proposal=proposal):
            role.delete()

        for reviewer in reviewers:
            reviewer.save()

        for bid in Bid.objects.filter(proposal=proposal):
            bid.delete()

        return Response({'status': 'Reviewer roles successfully assigned'})
