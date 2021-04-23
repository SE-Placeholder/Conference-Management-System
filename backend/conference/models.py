from django.db.models import Model, CharField, DateTimeField, FloatField


class Conference(Model):
    title = CharField(max_length=64)
    description = CharField(max_length=1024)
    location = CharField(max_length=64)
    date = DateTimeField()
    fee = FloatField()

    abstract_deadline = DateTimeField()
    proposal_deadline = DateTimeField()
    bidding_deadline = DateTimeField()

    def __str__(self):
        return f'{self.title} - {self.description}'

