from django.db import models

from conference.models import Conference


# TODO: custom filename to prevent path collision
class Paper(models.Model):
    title = models.CharField(max_length=64)
    conference = models.ForeignKey(Conference, related_name='papers', on_delete=models.CASCADE)

    topics = models.JSONField(blank=True, null=True)
    keywords = models.JSONField(blank=True, null=True)

    abstract = models.FileField(blank=True, null=True, upload_to='uploads/abstract/%Y/%m/%d/')
    proposal = models.FileField(blank=True, null=True, upload_to='uploads/proposal/%Y/%m/%d/')

    def __str__(self):
        return f'{self.title}'
