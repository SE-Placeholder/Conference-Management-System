from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from conference.models import Conference
from conference.serializers import ConferenceSerializer
from role.models import ListenerRole, SteeringCommitteeRole


# create conference: allow authenticated users
# list conferences: allow any
# update conference: allow only users with steering committee role for that conference
# retrieve conference: allow any
class ConferencePermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not bool(request.user and request.user.is_authenticated):
            return False
        return SteeringCommitteeRole.objects.filter(user=request.user, conference=obj).exists()


class ConferenceViewSet(ModelViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer
    permission_classes = [ConferencePermissions]
    lookup_field = 'id'


class JoinConferenceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            conference = Conference.objects.get(id=id)

            if ListenerRole.objects.filter(user=request.user, conference=conference).exists():
                return Response({'status': 'Already registered for this conference'},
                                status=status.HTTP_400_BAD_REQUEST)

            ListenerRole.objects.create(
                user=request.user,
                conference=conference)
            return Response({'status': 'Successfully joined conference'}, status=status.HTTP_201_CREATED)
        except Conference.DoesNotExist:
            return Response({'status': 'Conference does not exist'}, status=status.HTTP_404_NOT_FOUND)
