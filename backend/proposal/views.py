from rest_framework import status
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.utils import get_user
from proposal.models import Proposal, Bid
from proposal.serializers import ProposalSerializer, AssignReviewersSerializer
from role.models import AuthorRole, SteeringCommitteeRole, ReviewerRole


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


# TODO: this code makes me want to die, will refactor later
# TODO: use serializer
class BidProposalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            proposal = Proposal.objects.get(id=id)

            if not SteeringCommitteeRole.objects.filter(user=request.user, conference=proposal.conference).exists():
                return Response(
                    {'status': 'You need to be part of the steering committee to bid proposals'},
                    status=status.HTTP_401_UNAUTHORIZED)

            if 'qualifier' not in request.data:
                return Response(
                    {'status': 'Qualifier not found in request body'},
                    status=status.HTTP_400_BAD_REQUEST)

            try:
                qualifier = int(request.data['qualifier'])
                if qualifier not in [-1, 0, 1]:
                    return Response({'status': 'Qualifier should be either -1, 0 or 1'}, status=status.HTTP_400_BAD_REQUEST)

                for bid in Bid.objects.filter(user=request.user, proposal=proposal):
                    bid.delete()

                Bid.objects.create(
                    user=request.user,
                    proposal=proposal,
                    qualifier=qualifier)

            except ValueError:
                return Response({'status': 'Qualifier should be either -1, 0 or 1'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'status': 'Bid successfully submitted'}, status=status.HTTP_201_CREATED)

        except Proposal.DoesNotExist:
            return Response({'status': 'Proposal does not exist'}, status=status.HTTP_404_NOT_FOUND)


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
