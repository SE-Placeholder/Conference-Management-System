from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model, ForeignKey

from conference.models import Conference
from proposal.models import Proposal


class SteeringCommitteeRole(Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='committee')
    conference = ForeignKey(Conference, on_delete=models.CASCADE, related_name='committee')

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


class ReviewerRole(Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    proposal = ForeignKey(Proposal, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.proposal.title}'


class BidRole(Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name='bids')
    qualifier = models.SmallIntegerField(choices=[(-1, 'negative'), (0, 'neutral'), (1, 'positive')], null=True, blank=True)

    class Meta:
        unique_together = (("user", "proposal"),)

    def __str__(self):
        qualifiers = {-1: 'negative', 0: 'neutral', 1: 'positive'}
        return f'{self.user.username} bid {self.qualifier and qualifiers[self.qualifier] or "None"} for {self.proposal.title}'

