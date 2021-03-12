from django.db import models

from aagam_packages.django.model_extensions import models as amdl

from StudentPerformance.models import MapMySchoolUserSubject, TblSubject, MapMySchoolUserStandardSection
from MySchoolHome.models import MySchoolUser


# region Yash
class FeedbackManager(models.Manager):
    def retrive_feedback_forms(self, rate, com, user_id):
        forms = self.model.objects.all()
        r_c = self.model(feedback_rating=rate, feedback_comments=com, myschool_user=user_id)
        return forms, r_c

    def map_teacher_subject(self, sub):
        s = TblSubject.objects.get(subject_name=sub)
        mp = MapMySchoolUserSubject.objects.get(subject=s)
        ff = FeedbackForm.objects.get(subject_teacher=mp)
        ffq = FeedbackFormQuestion.objects.filter(feedback_form=ff)
        fbs = []
        for f in ffq:
            fb = Feedback.objects.filter(feedback_form_question=f)
            fbs.append(fb)
        return fbs
# endregion


# region Aagam Sheth
class FeedbackForm(amdl.AagamBaseModel):
    feedback_form_id = models.AutoField(primary_key=True)
    subject_teacher = models.ForeignKey(MapMySchoolUserSubject, models.DO_NOTHING)
    feedback_form_date = models.DateField()
    feedback_form_status = models.BooleanField()

    yash_objects = FeedbackManager()

    class Meta:
        db_table = 'feedback_form'

    def __str__(self):
        return f'{self.subject_teacher} : {self.feedback_form_date}'


class FeedbackFormQuestion(amdl.AagamBaseModel):
    feedback_form_question_id = models.AutoField(primary_key=True)
    feedback_form = models.ForeignKey('FeedbackForm', models.DO_NOTHING)
    feedback_question = models.ForeignKey('FeedbackQuestion', models.DO_NOTHING)

    yash_objects = FeedbackManager()

    class Meta:
        db_table = 'feedback_form_question'

    def __str__(self):
        return f'{self.feedback_form} : {self.feedback_question}'


class Feedback(amdl.AagamBaseModel):
    feedback_id = models.AutoField(primary_key=True)
    feedback_form_question = models.ForeignKey('FeedbackFormQuestion', models.DO_NOTHING)
    map_myschool_user_standard_section = models.ForeignKey(MapMySchoolUserStandardSection, models.DO_NOTHING)
    feedback_rating = models.IntegerField()
    feedback_comments = models.TextField()
    feedback_date = models.DateTimeField(auto_now_add=True)

    yash_objects = FeedbackManager()

    class Meta:
        db_table = 'feedback'

    def __str__(self):
        return f'{self.map_myschool_user_standard_section} : {self.feedback_form_question}'


class FeedbackQuestion(amdl.AagamBaseModel):
    feedback_question_id = models.AutoField(primary_key=True)
    question_text = models.TextField()
    feedback_question_credit = models.IntegerField()
    question_group = models.ForeignKey('FeedbackQuestionGroup', models.DO_NOTHING)

    yash_objects = FeedbackManager()

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
# endregion