from django.contrib.auth.models import User
from django.db import models

from conference.models import Conference


# TODO: custom filename to prevent path collision
class Proposal(models.Model):
    title = models.CharField(max_length=64)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)

    topics = models.JSONField(blank=True, null=True)
    keywords = models.JSONField(blank=True, null=True)

    abstract = models.FileField(blank=True, null=True, upload_to='abstract/')
    paper = models.FileField(blank=True, null=True, upload_to='paper/')

    def __str__(self):
        return f'{self.title}'
