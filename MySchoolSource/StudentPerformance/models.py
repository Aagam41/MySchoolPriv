from django.db import models
from django.contrib.auth.models import User

#TODO: Cascade Delete
class ChapterTopic(models.Model):
    chapter_topic_id = models.AutoField(primary_key=True)
    subject_chapter = models.ForeignKey('SubjectChapter', models.DO_NOTHING)
    topic_id = models.IntegerField()
    topic_name = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'chapter_topic'


class TblClass(models.Model):
    class_field = models.CharField(db_column='class', primary_key=True, max_length=3)  # Field renamed because it was a Python reserved word.
    describe = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'class'


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    student = models.ForeignKey('MySchoolUser', models.DO_NOTHING)
    map_teacher_subject = models.ForeignKey('MapTeacherSubject', models.DO_NOTHING)
    feedback_rating = models.IntegerField()
    feedback_comments = models.TextField()
    feedback_question = models.ForeignKey('FeedbackQuestion', models.DO_NOTHING)
    feedback_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'feedback'


class FeedbackQuestion(models.Model):
    feedback_question_id = models.AutoField(primary_key=True)
    question_text = models.TextField()
    feedback_question_credit = models.IntegerField()
    question_group = models.ForeignKey('FeedbackQuestionGroup', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'feedback_question'


class FeedbackQuestionGroup(models.Model):
    feedback_question_group_id = models.AutoField(primary_key=True)
    question_group = models.TextField()
    description = models.TextField()

    class Meta:
        managed = True
        db_table = 'feedback_question_group'

class MapTeacherSubject(models.Model):
    map_teacher_subject_id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey('MySchoolUser', models.DO_NOTHING)
    subject = models.ForeignKey('Tblsubject', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'map_myschool_user_subject'


class PaperPatternEntry(models.Model):
    paper_pattern_entry_id = models.AutoField(primary_key=True)
    paper_pattern_name = models.CharField(max_length=100)
    total_marks = models.IntegerField()
    subject = models.ForeignKey('Tblsubject', models.DO_NOTHING)
    marks_type = models.ForeignKey('MarksType', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'paper_pattern_entry'


class PaperPatternQuestion(models.Model):
    paper_pattern_question_id = models.AutoField(primary_key=True)
    paper_pattern_entry_id = models.ForeignKey('PaperPatternEntry', models.DO_NOTHING)
    paper_pattern_question_text_id = models.IntegerField() #TODO: Unique constraint with paperpatternid
    paper_pattern_question_text = models.TextField()
    rau_type = models.IntegerField()
    total_marks = models.IntegerField()
    chapter_topic = models.ForeignKey('ChapterTopic', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'paper_pattern_question'


class MapStudentPaperPatternQuestion(models.Model):
    student = models.ForeignKey('MySchoolUser',models.DO_NOTHING)
    paper_pattern_question = models.ForeignKey('PaperPatternQuestion', models.DO_NOTHING)
    mark_obtained = models.IntegerField() #TODO: Validation PaperPatternQuestion totalmarks <= this

    class Meta:
        managed = True
        db_table = "map_myschool_user_paper_pattern_question"


class MarksType(models.Model):
    marks_type_id = models.AutoField(primary_key=True)
    marks_type = models.CharField(max_length=100)
    out_of = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'marks_type'


class MySchoolUser(models.Model):
    myschool_user_id = models.AutoField(primary_key=True)
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)
    class_field = models.ForeignKey(TblClass, models.DO_NOTHING, db_column='class')  # Field renamed because it was a Python reserved word.
    role = models.ForeignKey('TblRole',models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'myschool_user'


class TblRole(models.Model):
    role_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50, null=True)

    class Meta:
        managed = True
        db_table ='tbl_role'


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
    student = models.ForeignKey('MySchoolUser', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'student_efficacy'


class SubjectChapter(models.Model):
    subject_chapter_id = models.AutoField(primary_key=True)
    subject = models.ForeignKey('Tblsubject', models.DO_NOTHING)
    chapter_id = models.IntegerField()
    chapter_name = models.CharField(max_length=15)
    remembarence_credit = models.IntegerField()
    applied_knowledge_credit = models.IntegerField()
    understanding_credit = models.IntegerField()
    chapter_credit = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'subject_chapter'


class Tblsubject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=20)
    class_field = models.ForeignKey(TblClass, models.DO_NOTHING, db_column='class')  # Field renamed because it was a Python reserved word.
    remembarence_credit = models.IntegerField()
    applied_knowledge_credit = models.IntegerField()
    understanding_credit = models.IntegerField()
    subject_credit = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'tblsubject'
