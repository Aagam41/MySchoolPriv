from django.db import models


class AagamBaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True
