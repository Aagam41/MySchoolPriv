from django.db import models
from django.contrib.auth.models import User

from aagam_packages.django_model_extensions import models as amdl


# Create your models here.


class MySchoolUser(amdl.AagamBaseModel):
    myschool_user_id = models.AutoField(primary_key=True)
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'myschool_user'
        constraints = [
            models.UniqueConstraint(fields=['auth_user'], name='unique_auth_user_for_myschool_user')
        ]

    def __str__(self):
        return f'{self.auth_user}'
