from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from paper.models import Paper
from paper.serializers import PaperSerializer
from role.models import AuthorRole


# create paper: allow authenticated users
# list papers: allow any
# update paper: allow only users with author role for that paper
# retrieve paper: allow any
class PaperPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not bool(request.user and request.user.is_authenticated):
            return False
        return AuthorRole.objects.filter(user=request.user, paper=obj).exists()


class PaperViewSet(ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
    permission_classes = [PaperPermissions]
    lookup_field = 'id'
