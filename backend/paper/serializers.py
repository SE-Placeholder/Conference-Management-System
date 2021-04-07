from rest_framework.serializers import ModelSerializer

from paper.models import Paper


class PaperSerializer(ModelSerializer):
    class Meta:
        model = Paper
        fields = ['id', 'title', 'author']
