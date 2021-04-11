from rest_framework.exceptions import ValidationError
from rest_framework.fields import ListField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from paper.models import Paper
from role.models import Role


class PaperSerializer(ModelSerializer):
    other_authors = ListField(write_only=True, required=False)
    authors = SerializerMethodField()

    class Meta:
        model = Paper
        fields = ['id', 'title', 'abstract', 'proposal', 'other_authors', 'authors']

    def create(self, validated_data):
        paper = Paper.objects.create(
            title=validated_data['title'],
            abstract=validated_data.get('abstract', None),
            proposal=validated_data.get('proposal', None),
        )
        paper.save()
        for author in validated_data.get('other_authors', []):
            print(author)
            # if author != '':
            #     raise ValidationError({"authors": "user not found"})
        return paper

    def get_authors(self, paper):
        return map(lambda role: role.user.username,
                   Role.objects.filter(role='author', paper=paper))
