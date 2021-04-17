from django.urls import path
from rest_framework.response import Response
from rest_framework.views import APIView

from conference.serializers import ConferenceSerializer
from role.models import Role, RoleTypes
from role.views import UserViewSet


class UserConferencesView(APIView):
    def get(self, request):
        user_roles = Role.objects.filter(user=request.user)

        steering_conferences = user_roles.filter(role=RoleTypes.STEERING_COMMITTEE)
        steering_conferences = map(lambda role: role.conference, steering_conferences)
        conference_serializer = ConferenceSerializer(steering_conferences, many=True)

        steering_conferences2 = user_roles.filter(role=RoleTypes.LISTENER)
        steering_conferences2 = map(lambda role: role.conference, steering_conferences2)
        conference_serializer2 = ConferenceSerializer(steering_conferences2, many=True)

        return Response({
            'steeringCommittee': conference_serializer.data,
            'listener': conference_serializer2.data
        })

        # try:
        #     conference = Conference.objects.get(id=id)
        #     Role.objects.create(
        #         role=RoleTypes.LISTENER,
        #         conference=conference,
        #         )
        #     return Response({'status': 'Successfully joined conference'}, status=status.HTTP_201_CREATED)
        # except Conference.DoesNotExist:
        #     pass
        # return Response({'status': 'Conference does not exist'}, status=status.HTTP_404_NOT_FOUND)


urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list'}), name='user-list'),
    # path('/<str:username>', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail')
    path('/conferences', UserConferencesView.as_view())
]
