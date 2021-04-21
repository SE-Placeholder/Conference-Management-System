from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from conference.models import Conference
from conference.serializers import ConferenceSerializer
from role.models import SteeringCommitteeRole, ListenerRole


class ConferenceViewSet(ModelViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer
    lookup_field = 'id'

    def get_permissions(self):
        return [AllowAny()] if self.action in ['list', 'retrieve'] else [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conference = serializer.save()

        SteeringCommitteeRole.objects.create(
            conference=conference,
            user=request.user)

        response = serializer.data
        response['steering_committee'] = map(lambda role: role.user.username, SteeringCommitteeRole.objects.filter(conference=conference))
        return Response(response, status=status.HTTP_201_CREATED)

    # TODO: allow only conference steering committee members to update conference
    def partial_update(self, request, *args, **kwargs):
        steering_committee = []
        errors = []
        for username in request.data.get('steering_committee', []):
            try:
                steering_committee.append(User.objects.get(username=username))
            except User.DoesNotExist:
                errors.append(f'user {username} not found.')

        if len(errors) != 0:
            return Response({'steering_committee': errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        conference = serializer.save()

        if 'steering_committee' in request.data:
            for role in SteeringCommitteeRole.objects.filter(conference=conference):
                role.delete()

        for user in steering_committee:
            SteeringCommitteeRole.objects.create(
                user=user,
                conference=conference)

        response = serializer.data
        response['steering_committee'] = map(lambda role: role.user.username, SteeringCommitteeRole.objects.filter(conference=conference))
        return Response(response, status=status.HTTP_200_OK)


class JoinConferenceView(APIView):
    def post(self, request, id):
        try:
            conference = Conference.objects.get(id=id)

            if ListenerRole.objects.filter(user=request.user, conference=conference).exists():
                return Response({'status': 'Already registered for this conference'}, status=status.HTTP_400_BAD_REQUEST)

            ListenerRole.objects.create(
                user=request.user,
                conference=conference)
            return Response({'status': 'Successfully joined conference'}, status=status.HTTP_201_CREATED)
        except Conference.DoesNotExist:
            return Response({'status': 'Conference does not exist'}, status=status.HTTP_404_NOT_FOUND)