from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from conference.models import Conference
from conference.serializers import ConferenceSerializer, JoinConferenceSerializer, JoinSectionSerializer
from role.models import SteeringCommitteeRole, ListenerRole


# create conference: allow authenticated users
# list conferences: allow any
# update conference: allow only users with steering committee role for that conference
# retrieve conference: allow any
class ConferencePermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not bool(request.user and request.user.is_authenticated):
            return False
        return SteeringCommitteeRole.objects.filter(user=request.user, conference=obj).exists()


class ConferenceViewSet(ModelViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer
    permission_classes = [ConferencePermissions]
    lookup_field = 'id'


# join conference: allow authenticated users
class JoinConferencePermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class JoinConferenceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        serializer = JoinConferenceSerializer(data=request.data)
        serializer.context['conference'] = get_object_or_404(Conference, id=id)
        serializer.context['user'] = request.user
        serializer.is_valid(raise_exception=True)
        # TODO: return this?
        listener_role = serializer.save()
        return Response({'detail': 'Successfully joined conference.'}, status=status.HTTP_201_CREATED)


# join section: allow authenticated users that have a listener role for the conference in which the section is organized
class JoinSectionPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_authenticated = bool(request.user and request.user.is_authenticated)
        return is_authenticated and ListenerRole.objects.filter(user=request.user, conference=obj).exists()


class JoinSectionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        serializer = JoinSectionSerializer(data=request.data)
        conference = get_object_or_404(Conference, id=id)
        # self.check_object_permissions(self.request, conference)
        serializer.context['conference'] = conference
        serializer.context['user'] = request.user
        serializer.is_valid(raise_exception=True)
        # TODO: return this?
        listener_role = serializer.save()
        return Response({'detail': 'Successfully joined section.'}, status=status.HTTP_201_CREATED)
