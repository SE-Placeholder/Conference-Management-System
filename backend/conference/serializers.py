from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer

from conference.models import Conference


class ConferenceSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Conference
        fields = ['id', 'title', 'description', 'deadline']