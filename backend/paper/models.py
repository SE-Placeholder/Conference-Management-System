from django.db import models


# TODO: change author to many to many relation or something
class Paper(models.Model):
    title = models.CharField(max_length=64)
    author = models.CharField(max_length=64)
