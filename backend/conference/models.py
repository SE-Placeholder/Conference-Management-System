from django.db.models import Model, CharField, DateTimeField, FloatField, ForeignKey, ManyToManyField
from django.db import models


class Conference(Model):
    title = CharField(max_length=64)
    description = CharField(max_length=1024)
    location = CharField(max_length=64)
    date = DateTimeField()
    fee = FloatField()

    abstract_deadline = DateTimeField()
    proposal_deadline = DateTimeField()
    bidding_deadline = DateTimeField()
    reviewing_deadline = DateTimeField()

    def __str__(self):
        return f'{self.title} - {self.description}'


class Section(Model):
    title = CharField(max_length=64)
    conference = ForeignKey(Conference, on_delete=models.CASCADE)
    start = DateTimeField()
    end = DateTimeField()
    # here be dragons
    from proposal.models import Proposal
    proposals = ManyToManyField(Proposal)
    # session_chair?

    def __str__(self):
        return f'{self.title} - {self.conference}'
