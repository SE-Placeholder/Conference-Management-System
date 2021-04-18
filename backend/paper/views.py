from rest_framework.viewsets import ModelViewSet

from paper.models import Paper
from paper.serializers import PaperSerializer


class PaperViewSet(ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
