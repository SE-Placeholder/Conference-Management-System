from rest_framework.viewsets import ViewSet, ModelViewSet

from conference.models import Conference
from conference.serializers import ConferenceSerializer


class ConferenceViewSet(ModelViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer
    lookup_field = 'id'