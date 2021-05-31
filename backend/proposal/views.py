from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from proposal.models import Proposal
from proposal.serializers import ProposalSerializer, AssignReviewersSerializer, BidProposalSerializer, \
    AddReviewSerializer
from role.models import AuthorRole, SteeringCommitteeRole


# create proposal: allow authenticated users
# list proposals: allow any
# update proposal: allow only users with author role for that proposal
# retrieve proposal: allow any
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


class ProposalViewSet(ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [ProposalPermissions]
    lookup_field = 'id'


# allow users that are authenticated and have steering committee role
class BidProposalPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_authenticated = bool(request.user and request.user.is_authenticated)
        is_steering_committee = SteeringCommitteeRole.objects.filter(
            user=request.user,
            conference=obj.proposal.conference
        ).exists()
        return is_authenticated and is_steering_committee


class BidProposalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        serializer = BidProposalSerializer(data=request.data)
        serializer.context['proposal'] = get_object_or_404(Proposal, id=id)
        serializer.context['user'] = request.user
        # self.check_object_permissions(self.request, proposal)
        serializer.is_valid(raise_exception=True)
        # TODO: return this?
        bid_role = serializer.save()
        return Response({'detail': 'Bid successfully submitted.'}, status=status.HTTP_201_CREATED)


class AssignReviewersPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_authenticated = bool(request.user and request.user.is_authenticated)
        is_steering_committee = SteeringCommitteeRole.objects.filter(
            user=request.user,
            conference=obj.proposal.conference
        ).exists()
        return is_authenticated and is_steering_committee


class AssignReviewersView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        serializer = AssignReviewersSerializer(data=request.data)
        serializer.context['proposal'] = get_object_or_404(Proposal, id=id)
        # self.check_object_permissions(self.request, proposal)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # TODO: return results
        return Response({'detail': 'Reviewers successfully assigned.'}, status=status.HTTP_201_CREATED)


# allow authenticated users that have reviewer role?
class AddReviewPermissions(BasePermission):
    pass
    # def has_object_permission(self, request, view, obj):
    #     is_authenticated = bool(request.user and request.user.is_authenticated)
    #     is_steering_committee = SteeringCommitteeRole.objects.filter(
    #         user=request.user,
    #         conference=obj.proposal.conference
    #     ).exists()
    #     return is_authenticated and is_steering_committee


class AddReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        serializer = AddReviewSerializer(data=request.data)
        serializer.context['user'] = request.user
        serializer.context['proposal'] = get_object_or_404(Proposal, id=id)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # TODO: return results
        return Response({'detail': 'Review successfully assigned.'}, status=status.HTTP_201_CREATED)
