from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from conference.serializers import ConferenceSerializer
from role.models import Role, RoleTypes


class UserConferencesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = Role.objects.filter(user=request.user)

        steering_committee_conferences = ConferenceSerializer(
            map(lambda role: role.conference,
                roles.filter(role=RoleTypes.STEERING_COMMITTEE)), many=True)

        listener_conferences = ConferenceSerializer(
            map(lambda role: role.conference,
                roles.filter(role=RoleTypes.LISTENER)), many=True)

        return Response({
            'steeringCommittee': steering_committee_conferences.data,
            'listener': listener_conferences.data
        }, status=status.HTTP_200_OK)


class UserPapersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = Role.objects.filter(user=request.user)
        