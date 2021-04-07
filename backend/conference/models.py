from django.db import models


class Conference(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    deadline = models.DateTimeField()

    def __str__(self):
        return f'{self.title} - {self.description[:32]}'

