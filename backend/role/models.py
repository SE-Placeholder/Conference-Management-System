from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model, ForeignKey, CharField, ManyToManyField

from conference.models import Conference, Section
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
    sections = ManyToManyField(Section)

    def __str__(self):
        return f'{self.user.username} - {self.conference.title}'


class ReviewerRole(Model):
    qualifier_choices = [(-3, 'strong reject'), (-2, 'reject'), (-1, 'weak reject'),
                         (0, 'borderline'), (1, 'weak accept'), (2, 'accept'), (3, 'strong accept')]
    user = ForeignKey(User, on_delete=models.CASCADE)
    proposal = ForeignKey(Proposal, on_delete=models.CASCADE)
    review = CharField(max_length=1024, null=True, blank=True)
    qualifier = models.SmallIntegerField(choices=qualifier_choices, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} rated {self.proposal.title} with {self.get_qualifier_display()}'


class BidRole(Model):
    qualifier_choices = [(-1, 'negative'), (0, 'neutral'), (1, 'positive')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name='bids')
    qualifier = models.SmallIntegerField(choices=qualifier_choices, null=True, blank=True)

    class Meta:
        unique_together = (("user", "proposal"),)

    def __str__(self):
        return f'{self.user.username} bid {self.get_qualifier_display()} for {self.proposal.title}'

