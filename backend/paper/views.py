from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from paper.models import Paper
from paper.serializers import PaperSerializer
from role.models import Role, RoleTypes


class PaperViewSet(ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        authors = [request.user]
        errors = []
        for username in request.data.get('authors', []):
            try:
                authors.append(User.objects.get(username=username))
            except User.DoesNotExist:
                errors.append(f'user {username} not found.')

        if len(errors) != 0:
            return Response({'authors': errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        paper = serializer.save()

        for user in authors:
            Role.objects.create(
                role=RoleTypes.AUTHOR,
                user=user,
                paper=paper)

        response = serializer.data
        response['authors'] = map(lambda role: role.user.username, Role.objects.filter(role=RoleTypes.AUTHOR, paper=paper))
        return Response(response, status=status.HTTP_201_CREATED)

    # TODO: allow only authors to update conference
    def partial_update(self, request, *args, **kwargs):
        authors = []
        errors = []
        for username in request.data.get('authors', []):
            try:
                authors.append(User.objects.get(username=username))
            except User.DoesNotExist:
                errors.append(f'user {username} not found.')

        if len(errors) != 0:
            return Response({'authors': errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        paper = serializer.save()

        if 'authors' in request.data:
            for role in Role.objects.filter(role=RoleTypes.AUTHOR, paper=paper):
                role.delete()

        for user in authors:
            Role.objects.create(
                role=RoleTypes.AUTHOR,
                user=user,
                paper=paper)

        response = serializer.data
        response['authors'] = map(lambda role: role.user.username, Role.objects.filter(role=RoleTypes.AUTHOR, paper=paper))
        return Response(response, status=status.HTTP_200_OK)
