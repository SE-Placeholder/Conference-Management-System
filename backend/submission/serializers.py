from rest_framework.exceptions import ValidationError
from rest_framework.fields import JSONField
from rest_framework.serializers import ModelSerializer

from api.utils import get_user
from submission.models import Paper
from role.models import AuthorRole
from role.serializers import UserSerializer


class PaperSerializer(ModelSerializer):
    authors = JSONField(binary=True, write_only=True, required=False)

    class Meta:
        model = Paper
        fields = ['id', 'title', 'conference', 'topics', 'keywords', 'abstract', 'paper', 'authors']

    def create(self, validated_data):
        authors = [self.context['request'].user]
        errors = []

        for user_id in list(set(validated_data.pop('authors', []))):
            user = get_user(user_id)
            if user:
                authors.append(user)
            else:
                errors.append(f'user {user_id} not found.')

        if errors:
            raise ValidationError({'authors': errors})

        paper = super().create(validated_data)

        for user in authors:
            AuthorRole.objects.create(
                user=user,
                paper=paper)

        return paper

    def update(self, instance, validated_data):
        authors = []
        errors = []

        for user_id in list(set(validated_data.pop('authors', []))):
            user = get_user(user_id)
            if user:
                authors.append(user)
            else:
                errors.append(f'user {user_id} not found.')

        if errors:
            raise ValidationError({'authors': errors})

        paper = super().update(instance, validated_data)

        if authors:
            for role in AuthorRole.objects.filter(paper=paper):
                role.delete()

        for user in authors:
            AuthorRole.objects.create(user=user, paper=paper)

        return paper

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['authors'] = UserSerializer(
            map(lambda role: role.user, AuthorRole.objects.filter(paper=instance)),
            many=True).data
        return representation
