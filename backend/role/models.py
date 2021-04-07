from django.contrib.auth.models import User
from django.db import models

from conference.models import Conference
from paper.models import Paper


# TODO: i have no idea what to use for on_delete fields
class Role(models.Model):
    # TODO: replace with foreign key?
    role = models.CharField(max_length=32)

    conference = models.ForeignKey(Conference, default=None, related_name='conference', on_delete=models.CASCADE, blank=True, null=True)
    paper = models.ForeignKey(Paper, default=None, related_name='paper', on_delete=models.CASCADE, blank=True, null=True)

    user = models.ForeignKey(User, related_name='roles', on_delete=models.CASCADE)