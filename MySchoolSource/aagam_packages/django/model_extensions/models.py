from django.db import models
from django.urls import reverse


class AagamBaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        managed = True
        abstract = True

    def get_absolute_url(self):
        return reverse('MySchoolHome:home')
