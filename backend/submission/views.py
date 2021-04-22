from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from submission.models import Submission
from submission.serializers import SubmissionSerializer
from role.models import AuthorRole


# create submission: allow authenticated users
# list submissions: allow any
# update submission: allow only users with author role for that submission
# retrieve submission: allow any
class SubmissionPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not bool(request.user and request.user.is_authenticated):
            return False
        return AuthorRole.objects.filter(user=request.user, submission=obj).exists()


class SubmissionViewSet(ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [SubmissionPermissions]
    lookup_field = 'id'
