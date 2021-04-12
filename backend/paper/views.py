from rest_framework.viewsets import ModelViewSet

from paper.models import Paper
from paper.serializers import PaperSerializer


class PaperViewSet(ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
    # lookup_field = 'id'

    # def create(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    #     conference = serializer.save()
    #     # TODO: don't hardcode this
    #     role = Role(role='steering committee', conference=conference, user=self.request.user)
    #     role.save()
    #
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)