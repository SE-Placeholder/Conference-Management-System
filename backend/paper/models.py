from django.db import models

from conference.models import Conference


class Paper(models.Model):
    title = models.CharField(max_length=64)
    # TODO: custom filename to prevent path collision
    abstract = models.FileField(blank=True, null=True, upload_to='uploads/abstract/%Y/%m/%d/')
    proposal = models.FileField(blank=True, null=True, upload_to='uploads/proposal/%Y/%m/%d/')
    conference = models.ForeignKey(Conference, related_name='papers', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'
