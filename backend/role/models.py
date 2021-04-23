from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model, ForeignKey

from conference.models import Conference
from proposal.models import Proposal


class SteeringCommitteeRole(Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    conference = ForeignKey(Conference, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.conference.title}'


class AuthorRole(Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    proposal = ForeignKey(Proposal, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.proposal.title}'


class ListenerRole(Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    conference = ForeignKey(Conference, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.conference.title}'