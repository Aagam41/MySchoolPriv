from django.db import models

from aagam_packages.django.model_extensions import models as amdl

from MySchoolHome.models import MySchoolUser


# Create your models here.


class StudentEfficacy(amdl.AagamBaseModel):
    student_efficacy_id = models.AutoField(primary_key=True)
    father_education = models.IntegerField()
    internet_facility = models.IntegerField()
    study_time = models.IntegerField()
    paid_tuition = models.IntegerField()
    past_failures = models.IntegerField()
    free_time = models.IntegerField()
    extra_curricular_activities = models.IntegerField()
    absences = models.IntegerField()
    class_engagement = models.IntegerField()
    health = models.IntegerField()
    student = models.ForeignKey(MySchoolUser, models.DO_NOTHING)
    past_marks = models.IntegerField()
    past_marks1 = models.IntegerField()
    predictons = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'student_efficacy'

    def __str__(self):
        return str(self.student)
