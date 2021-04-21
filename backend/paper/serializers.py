from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ListField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from paper.models import Paper
from role.models import AuthorRole


class PaperSerializer(ModelSerializer):
    authors = SerializerMethodField()

    class Meta:
        model = Paper
        fields = [
            'id',
            'title',
            'conference',
            'topics',
            'keywords',
            'abstract',
            'proposal',
            'authors'
        ]

    @staticmethod
    def get_authors(paper):
        return map(lambda role: role.user.username,
                   AuthorRole.objects.filter(paper=paper))
