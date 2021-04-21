from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from conference.models import Conference
from paper.models import Paper
from paper.serializers import PaperSerializer
from role.models import SteeringCommitteeRole
from role.serializers import UserSerializer


class ConferenceSerializer(ModelSerializer):
    steering_committee = SerializerMethodField()
    papers = SerializerMethodField()

    class Meta:
        model = Conference
        fields = [
            'id',
            'title',
            'description',
            'deadline',
            'location',
            'date',
            'fee',
            'steering_committee',
            'papers'
        ]

    @staticmethod
    def get_steering_committee(conference):
        steering_committee = UserSerializer(
            map(lambda role: role.user,
                SteeringCommitteeRole.objects.filter(conference=conference)),
            many=True)
        return steering_committee.data

    @staticmethod
    def get_papers(conference):
        papers = PaperSerializer(
            Paper.objects.filter(conference=conference),
            many=True)
        return papers.data
