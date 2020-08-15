from django.db import models

# Create your models here.
class ChapterTopic(models.Model):
    chapter_topic_id = models.AutoField(primary_key=True)
    subject_chapter = models.ForeignKey('SubjectChapter', models.DO_NOTHING)
    topic_id = models.IntegerField()
    topic_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'chapter_topic'


class TblClass(models.Model):
    class_field = models.CharField(db_column='class', primary_key=True, max_length=3)  # Field renamed because it was a Python reserved word.
    describe = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'class'


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    student = models.ForeignKey('Student', models.DO_NOTHING)
    map_teacher_subject = models.ForeignKey('MapTeacherSubject', models.DO_NOTHING)
    feedback_rating = models.IntegerField()
    feedback_comments = models.TextField()
    feedback_question = models.ForeignKey('FeedbackQuestion', models.DO_NOTHING)
    feedback_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'feedback'


class FeedbackQuestion(models.Model):
    feedback_question_id = models.AutoField(primary_key=True)
    question_text = models.TextField()
    feedback_question_credit = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'feedback_question'


class MapTeacherSubject(models.Model):
    map_teacher_subject_id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey('Teacher', models.DO_NOTHING)
    subject = models.ForeignKey('Tblsubject', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'map_teacher_subject'


class MarksObtained(models.Model):
    marks_id = models.AutoField(primary_key=True)
    marks_gained = models.IntegerField()
    chapter_topic = models.ForeignKey(ChapterTopic, models.DO_NOTHING)
    student = models.ForeignKey('Student', models.DO_NOTHING)
    marks_type = models.ForeignKey('MarksType', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'marks_obtained'


class MarksType(models.Model):
    marks_type_id = models.AutoField(primary_key=True)
    marks_type = models.CharField(max_length=100)
    out_of = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'marks_type'


class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_no = models.BigIntegerField()
    email_id = models.CharField(max_length=100)
    password = models.TextField()
    salt = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'person'


class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'staff'


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person, models.DO_NOTHING)
    class_field = models.ForeignKey(TblClass, models.DO_NOTHING, db_column='class')  # Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'student'


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
    student = models.ForeignKey(Student, models.DO_NOTHING)

    class Meta:
        managed = False
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
        managed = False
        db_table = 'subject_chapter'


class Tblrole(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_type = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'tblrole'


class Tblsubject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=20)
    class_field = models.ForeignKey(TblClass, models.DO_NOTHING, db_column='class')  # Field renamed because it was a Python reserved word.
    remembarence_credit = models.IntegerField()
    applied_knowledge_credit = models.IntegerField()
    understanding_credit = models.IntegerField()
    subject_credit = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tblsubject'


class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'teacher'