from django.db import models

from aagam_packages.django_model_extensions import models as amdl

from StudentPerformance.models import MapMySchoolUserSubject
from MySchoolHome.models import MySchoolUser


# Create your models here.


class FeedbackForm(amdl.AagamBaseModel):
    feedback_form_id = models.AutoField(primary_key=True)
    subject_teacher = models.ForeignKey(MapMySchoolUserSubject, models.DO_NOTHING)
    feedback_form_date = models.DateField()
    feedback_form_status = models.BooleanField()

    class Meta:
        db_table = 'feedback_form'

    def __str__(self):
        return f'{self.subject_teacher} : {self.feedback_form_date}'


class FeedbackFormQuestion(amdl.AagamBaseModel):
    feedback_form_question_id = models.AutoField(primary_key=True)
    feedback_form = models.ForeignKey('FeedbackForm', models.DO_NOTHING)
    feedback_question = models.ForeignKey('FeedbackQuestion', models.DO_NOTHING)

    class Meta:
        db_table = 'feedback_form_question'

    def __str__(self):
        return f'{self.feedback_form} : {self.feedback_question}'


class Feedback(amdl.AagamBaseModel):
    feedback_id = models.AutoField(primary_key=True)
    feedback_form_question = models.ForeignKey('FeedbackFormQuestion', models.DO_NOTHING)
    myschool_user = models.ForeignKey(MySchoolUser, models.DO_NOTHING)
    feedback_rating = models.IntegerField()
    feedback_comments = models.TextField()
    feedback_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'feedback'

    def __str__(self):
        return f'{self.myschool_user} : {self.feedback_form_question}'


class FeedbackQuestion(amdl.AagamBaseModel):
    feedback_question_id = models.AutoField(primary_key=True)
    question_text = models.TextField()
    feedback_question_credit = models.IntegerField()
    question_group = models.ForeignKey('FeedbackQuestionGroup', models.DO_NOTHING)

    class Meta:
        db_table = 'feedback_question'

    def __str__(self):
        return f'{self.question_group} : {self.question_text}'


class FeedbackQuestionGroup(amdl.AagamBaseModel):
    feedback_question_group_id = models.AutoField(primary_key=True)
    question_group = models.TextField()
    description = models.TextField()

    class Meta:
        db_table = 'feedback_question_group'

    def __str__(self):
        return self.question_group
