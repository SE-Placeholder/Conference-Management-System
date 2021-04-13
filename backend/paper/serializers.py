from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ListField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from paper.models import Paper
from role.models import Role, RoleTypes


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
        for author in validated_data.get('other_authors', []) + [self.context['request'].user.username]:
            try:
                user = User.objects.get(username=author)
                Role.objects.create(
                    role=RoleTypes.AUTHOR,
                    paper=paper,
                    user=user)
            except User.DoesNotExist:
                print('user does not exist ' + author)
                # TODO: return error with list of users that don't exist
                # raise ValidationError({"authors": "user not found"})

        return paper

    def get_authors(self, paper):
        return map(lambda role: role.user.username,
                   Role.objects.filter(role=RoleTypes.AUTHOR, paper=paper))
