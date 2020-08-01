from django.db import models

# Create your models here.
class AssessmentCreditObtained(models.Model):
    assessmet_credit_obtained_id = models.AutoField(primary_key=True)
    assessment_type = models.ForeignKey('AssessmentType', models.DO_NOTHING)
    map_student_subject = models.ForeignKey('MapSubjectStudent', models.DO_NOTHING)
    credit_obtained = models.IntegerField()
    flag_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'assessment_credit_obtained'


class AssessmentType(models.Model):
    assessment_type_id = models.AutoField(primary_key=True)
    assessment_type = models.TextField()
    total_marks = models.IntegerField()
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'assessment_type'


class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_code = models.IntegerField()
    department_name = models.TextField()
    department_head = models.TextField()
    no_semester = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'department'


class Educator(models.Model):
    educator_id = models.AutoField(primary_key=True)
    educator_name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, models.DO_NOTHING)
    date_of_birth = models.DateField()
    email_address = models.CharField(max_length=50)
    phone_no = models.BigIntegerField()
    gender = models.IntegerField()
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    status = models.IntegerField()
    role = models.ForeignKey('MstRole', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'educator'


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    lecture = models.ForeignKey('Lecture', models.DO_NOTHING)
    student = models.ForeignKey('Student', models.DO_NOTHING)
    feedback_question = models.ForeignKey('FeedbackQuestion', models.DO_NOTHING)
    rating = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'feedback'


class FeedbackQuestion(models.Model):
    question_id = models.AutoField(primary_key=True)
    question = models.TextField()
    out_of = models.IntegerField()
    question_type = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'feedback_question'


class Lecture(models.Model):
    lecture_id = models.AutoField(primary_key=True)
    educator = models.ForeignKey(Educator, models.DO_NOTHING)
    syllabus_topic = models.ForeignKey('SyllabusTopic', models.DO_NOTHING)
    semester = models.IntegerField()
    lecture_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'lecture'


class MapSubjectStudent(models.Model):
    ma_subject_student_id = models.AutoField(primary_key=True)
    subject = models.ForeignKey('Subject', models.DO_NOTHING)
    student = models.ForeignKey('Student', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'map_subject_student'


class MapSubjectTeacher(models.Model):
    map_subject_teacher_id = models.AutoField(primary_key=True)
    subject_id = models.TextField()
    educator_id = models.TextField()

    class Meta:
        managed = False
        db_table = 'map_subject_teacher'


class MstRole(models.Model):
    role_id = models.IntegerField(primary_key=True)
    role_name = models.CharField(unique=True, max_length=45)
    role_description = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_role'


class Parent(models.Model):
    parent_id = models.AutoField(primary_key=True)
    parent_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email_address = models.CharField(max_length=50)
    phone_no = models.BigIntegerField()
    gender = models.IntegerField()
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'parent'


class Staff(models.Model):
    staff_id = models.AutoField(db_column='staff__id', primary_key=True)  # Field renamed because it contained more than one '_' in a row.
    staff_name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, models.DO_NOTHING)
    date_of_birth = models.DateField()
    email_address = models.CharField(max_length=50)
    phone_no = models.BigIntegerField()
    gender = models.IntegerField()
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    status = models.IntegerField()
    role = models.ForeignKey(MstRole, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'staff'


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(Parent, models.DO_NOTHING)
    student_name = models.CharField(max_length=50)
    department_id = models.CharField(max_length=50)
    semester = models.IntegerField()
    date_of_birth = models.DateField()
    email_address = models.CharField(max_length=50)
    phone_no = models.BigIntegerField()
    gender = models.IntegerField()
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    credits_earned = models.IntegerField(blank=True, null=True)
    grade_average_point = models.IntegerField(blank=True, null=True)
    status = models.IntegerField()
    role = models.ForeignKey(MstRole, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'student'


class StudentEfficacy(models.Model):
    student_efficacy_id = models.AutoField(primary_key=True)
    family_size = models.IntegerField()
    mother_education = models.IntegerField()
    father_education = models.IntegerField()
    school_reason = models.IntegerField()
    study_time = models.IntegerField()
    past_failures = models.IntegerField()
    paid_tution = models.IntegerField()
    internet_access = models.IntegerField()
    free_time = models.IntegerField()
    absences = models.IntegerField()
    class_engagement = models.IntegerField()
    student = models.ForeignKey(Student, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'student_efficacy'


class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Department, models.DO_NOTHING)
    semetser_id = models.IntegerField()
    subject_code = models.IntegerField()
    subject_name = models.CharField(max_length=50)
    subject_credit = models.IntegerField()
    remembering_credit = models.IntegerField()
    undertsanging_credit = models.IntegerField()
    applied_knowledge_credit = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'subject'


class Syllabus(models.Model):
    syllabus_id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, models.DO_NOTHING)
    unit_id = models.IntegerField()
    unit_name = models.CharField(max_length=50)
    remembering_credit = models.IntegerField()
    undertsanging_credit = models.IntegerField()
    applied_knowledge_credit = models.IntegerField()
    unit_credit = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'syllabus'


class SyllabusTopic(models.Model):
    map_syllabus_topic_id = models.AutoField(primary_key=True)
    syllabus = models.ForeignKey(Syllabus, models.DO_NOTHING)
    topic_id = models.IntegerField()
    topic_name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'syllabus_topic'
