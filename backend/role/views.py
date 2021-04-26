from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from conference.models import Conference
from conference.serializers import ConferenceSerializer
from proposal.views import BidPermissions
from role.models import SteeringCommitteeRole, ListenerRole, AuthorRole


class UserConferencesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        steering_committee_conferences = ConferenceSerializer(
            map(lambda role: role.conference,
                SteeringCommitteeRole.objects.filter(user=request.user)), many=True)

        listener_conferences = ConferenceSerializer(
            map(lambda role: role.conference,
                ListenerRole.objects.filter(user=request.user)), many=True)

        return Response({
            'steeringCommittee': steering_committee_conferences.data,
            'listener': listener_conferences.data
        }, status=status.HTTP_200_OK)


class UserProposalsView(APIView):
    permission_classes = [IsAuthenticated, BidPermissions]

    def get(self, request):
        roles = AuthorRole.objects.filter(user=request.user)

        conferences = {}

        for role in roles:
            proposal = role.proposal
            conference = proposal.conference
            if conference.id not in conferences:
                conferences[conference.id] = []
            conferences[conference.id].append({
                'title': proposal.title
            })

        data = []
        for conferenceid, proposals in conferences.items():
            data.append({
                'id': conferenceid,
                'title': Conference.objects.get(id=conferenceid).title,
                'proposals': proposals
            })

        return Response(data, status=status.HTTP_200_OK)
