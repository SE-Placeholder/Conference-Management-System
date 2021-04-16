from django.urls import path
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from conference.models import Conference
from conference.views import ConferenceViewSet
from role.models import Role, RoleTypes


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

urlpatterns = [
    path('', ConferenceViewSet.as_view({'get': 'list', 'post': 'create'}), name='conference-list'),
    # TODO: update and delete
    path('/<int:id>', ConferenceViewSet.as_view({'get': 'retrieve'}), name='conference-detail'),
    path('/<int:id>/join', JoinConferenceView.as_view())
]