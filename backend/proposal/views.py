from rest_framework import status
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from proposal.models import Proposal, Bid
from proposal.serializers import ProposalSerializer
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


# TODO: this code makes me want to die, will refactor later
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

                Bid.objects.create(
                    user=request.user,
                    proposal=proposal,
                    qualifier=qualifier
                )
            except ValueError:
                return Response({'status': 'Qualifier should be either -1, 0 or 1'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'status': 'Bid successfully submitted'}, status=status.HTTP_201_CREATED)

        except Proposal.DoesNotExist:
            return Response({'status': 'Proposal does not exist'}, status=status.HTTP_404_NOT_FOUND)
