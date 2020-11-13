from django.db import models
from MySchoolHome.models import MySchoolUser

# Create your models here.


class StudentEfficacy(models.Model):
    student_efficacy_id = models.AutoField(primary_key=True)
    father_education = models.IntegerField()
    mother_education = models.IntegerField()
    internet_facility = models.IntegerField()
    study_time = models.IntegerField()
    paid_tution = models.IntegerField()
    past_failures = models.IntegerField()
    free_time = models.IntegerField()
    extra_curricular_activties = models.IntegerField()
    absences = models.IntegerField()
    class_engagement = models.IntegerField()
    health = models.IntegerField()
    student = models.ForeignKey(MySchoolUser, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'student_efficacy'

    def __str__(self):
        return self.student
