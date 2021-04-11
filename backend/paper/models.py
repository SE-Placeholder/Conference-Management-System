from django.db import models


class Paper(models.Model):
    title = models.CharField(max_length=64)
    # TODO: custom filename to prevent path collision
    abstract = models.FileField(blank=True, null=True, upload_to='uploads/abstract/%Y/%m/%d/')
    proposal = models.FileField(blank=True, null=True, upload_to='uploads/proposal/%Y/%m/%d/')

    def __str__(self):
        return f'{self.title}'
