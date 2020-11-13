from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MySchoolUser(models.Model):
    myschool_user_id = models.AutoField(primary_key=True)
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey('Role', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'myschool_user'

    def __str__(self):
        return f'{self.auth_user} : {self.role}'


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50, null=True)

    class Meta:
        managed = True
        db_table = 'enum_role'

    def __str__(self):
        return self.description
