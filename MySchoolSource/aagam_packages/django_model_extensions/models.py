from django.db import models


class AagamBaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        managed = True
        abstract = True
