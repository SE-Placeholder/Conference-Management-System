from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from proposal.models import Proposal
from proposal.serializers import ProposalSerializer
from role.models import AuthorRole


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
