from enum import IntEnum

from django.contrib.auth.models import User
from django.db import models

from conference.models import Conference
from paper.models import Paper


class RoleTypes(IntEnum):
    STEERING_COMMITTEE = 1
    AUTHOR = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Role(models.Model):
    role = models.IntegerField(choices=RoleTypes.choices())
    user = models.ForeignKey(User, related_name='roles', on_delete=models.CASCADE)

    conference = models.ForeignKey(Conference, default=None, related_name='conference', on_delete=models.CASCADE, blank=True, null=True)
    paper = models.ForeignKey(Paper, default=None, related_name='paper', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'[{self.get_role_display()}] {self.user}'
