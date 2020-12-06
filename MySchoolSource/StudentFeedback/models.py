from django.db import models
from StudentPerformance.models import MapTeacherSubject
from MySchoolHome.models import MySchoolUser


# Create your models here.


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(MySchoolUser, models.DO_NOTHING)
    map_teacher_subject = models.ForeignKey(MapTeacherSubject, models.DO_NOTHING)
    feedback_rating = models.IntegerField()
    feedback_comments = models.TextField()
    feedback_question = models.ForeignKey('FeedbackQuestion', models.DO_NOTHING)
    feedback_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'feedback'
        constraints = [
            models.UniqueConstraint(fields=['student', 'map_teacher_subject', 'feedback_question', 'feedback_date'],
                                    name='unique_for_student_feedback_on_subject_teacher'),
            ]

    def __str__(self):
        return self.feedback_id


class FeedbackQuestion(models.Model):
    feedback_question_id = models.AutoField(primary_key=True)
    question_text = models.TextField()
    feedback_question_credit = models.IntegerField()
    question_group = models.ForeignKey('FeedbackQuestionGroup', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'feedback_question'

    def __str__(self):
        return f'{self.question_group} : {self.question_text}'


class FeedbackQuestionGroup(models.Model):
    feedback_question_group_id = models.AutoField(primary_key=True)
    question_group = models.TextField()
    description = models.TextField()

    class Meta:
        managed = True
        db_table = 'feedback_question_group'

    def __str__(self):
        return self.question_group
