from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from conference.models import Conference
from conference.serializers import ConferenceSerializer
from role.models import RoleTypes, Role


class ConferenceViewSet(ModelViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer
    lookup_field = 'id'


class JoinConferenceView(APIView):
    def post(self, request, id):
        try:
            conference = Conference.objects.get(id=id)
            Role.objects.create(
                role=RoleTypes.LISTENER,
                conference=conference,
                user=request.user)
            return Response({'status': 'Successfully joined conference'}, status=status.HTTP_201_CREATED)
        except Conference.DoesNotExist:
            pass
        return Response({'status': 'Conference does not exist'}, status=status.HTTP_404_NOT_FOUND)