from rest_framework.serializers import ModelSerializer

from conference.models import Conference


# TODO: change to hyperlinked model serializer
class ConferenceSerializer(ModelSerializer):
    # url = HyperlinkedIdentityField(view_name='conference-detail', lookup_field='pk')
    class Meta:
        model = Conference
        fields = ['id', 'title', 'description', 'deadline']
