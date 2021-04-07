from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView

from conference.models import Conference
from conference.serializers import ConferenceSerializer


class ListConferencesView(ListAPIView):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer


class GetConferenceView(RetrieveAPIView):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer
    lookup_field = 'id'


class AddConferenceView(CreateAPIView):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer
