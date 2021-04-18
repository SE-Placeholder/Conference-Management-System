from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ListField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from paper.models import Paper
from role.models import Role, RoleTypes


class PaperSerializer(ModelSerializer):
    contributors = ListField(write_only=True, required=False)
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
            'contributors',  # WRITE-ONLY
            'authors',  # READ-ONLY
        ]

    def create(self, validated_data):
        paper = Paper(
            title=validated_data['title'],
            conference=validated_data['conference'],
            abstract=validated_data.get('abstract', None),
            proposal=validated_data.get('proposal', None),
            keywords=validated_data.get('keywords', None),
            topics=validated_data.get('topics', None)
        )
        authors = [self.context['request'].user.username] + validated_data.get('contributors', [])
        roles = []
        errors = []
        for author in authors:
            try:
                role = Role(
                    role=RoleTypes.AUTHOR,
                    paper=paper,
                    user=User.objects.get(username=author)
                )
                roles.append(role)
            except User.DoesNotExist:
                errors.append({"authors": f"user '{author}' not found"})

        if len(errors) == 0:
            paper.save()
            for role in roles:
                role.save()
        else:
            raise ValidationError({'authors': errors})

        return paper

    @staticmethod
    def get_authors(paper):
        return map(lambda role: role.user.username,
                   Role.objects.filter(role=RoleTypes.AUTHOR, paper=paper))
