from django.db import models
from MySchoolHome.models import MySchoolUser

# TODO: Cascade Delete


class ChapterTopic(models.Model):
    chapter_topic_id = models.AutoField(primary_key=True)
    subject_chapter = models.ForeignKey('SubjectChapter', models.DO_NOTHING)
    topic_id = models.IntegerField()
    topic_name = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'chapter_topic'

    def __str__(self):
        return f'{self.topic_id}. {self.topic_name}'


class Standard(models.Model):
    standard = models.IntegerField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'standard'

    def __str__(self):
        return str(self.standard)


class StandardSection(models.Model):
    standard_section_id = models.AutoField(primary_key=True)
    standard = models.ForeignKey(Standard, models.DO_NOTHING)
    section = models.CharField(max_length=1)

    class Meta:
        managed = True
        db_table = 'standard_section'

    def __str__(self):
        return f'{self.standard} {self.section}'


class MapTeacherSubject(models.Model):
    map_teacher_subject_id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(MySchoolUser, models.DO_NOTHING)
    subject = models.ForeignKey('Tblsubject', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'map_myschool_user_subject'

    def __str__(self):
        return f'{self.subject} {self.teacher}'


class PaperPatternEntry(models.Model):
    paper_pattern_entry_id = models.AutoField(primary_key=True)
    paper_pattern_name = models.CharField(max_length=100)
    total_marks = models.IntegerField()
    subject = models.ForeignKey('Tblsubject', models.DO_NOTHING)
    marks_type = models.ForeignKey('MarksType', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'paper_pattern_entry'

    def __str__(self):
        return self.paper_pattern_name


class PaperPatternQuestion(models.Model):
    paper_pattern_question_id = models.AutoField(primary_key=True)
    paper_pattern_entry_id = models.ForeignKey('PaperPatternEntry', models.DO_NOTHING)
    paper_pattern_question_text_id = models.IntegerField()  # TODO: Unique constraint with paperpatternid
    paper_pattern_question_text = models.TextField()
    rau_type = models.IntegerField()
    total_marks = models.IntegerField()
    chapter_topic = models.ForeignKey('ChapterTopic', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'paper_pattern_question'

    def __str__(self):
        return self.paper_pattern_question_text


class MapStudentPaperPatternQuestion(models.Model):
    map_student_paper_pattern_question_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(MySchoolUser, models.DO_NOTHING)
    paper_pattern_question = models.ForeignKey('PaperPatternQuestion', models.DO_NOTHING)
    marks_obtained = models.IntegerField()  # TODO: Validation PaperPatternQuestion totalmarks <= this

    class Meta:
        managed = True
        db_table = "map_myschool_user_paper_pattern_question"

    def __str__(self):
        return self.map_student_paper_pattern_question_id


class MapMySchoolUserStandardSection(models.Model):
    map_my_school_user_standard_section = models.AutoField(primary_key=True)
    myschool_user = models.ForeignKey(MySchoolUser, models.DO_NOTHING)
    standard_section = models.ForeignKey(StandardSection, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "map_myschool_user_standard_section"

    def __str__(self):
        return f'{self.standard_section} {self.myschool_user}'


class MarksType(models.Model):
    marks_type_id = models.AutoField(primary_key=True)
    marks_type = models.CharField(max_length=100)
    out_of = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'marks_type'

    def __str__(self):
        return self.marks_type


class SubjectChapter(models.Model):
    subject_chapter_id = models.AutoField(primary_key=True)
    subject = models.ForeignKey('Tblsubject', models.DO_NOTHING)
    chapter_id = models.IntegerField()
    chapter_name = models.CharField(max_length=15)
    remembrance_credit = models.IntegerField()
    applied_knowledge_credit = models.IntegerField()
    understanding_credit = models.IntegerField()
    chapter_credit = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'subject_chapter'

    def __str__(self):
        return f'{self.chapter_id} {self.chapter_name}'


class Tblsubject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=20)
    standard = models.ForeignKey(Standard, models.DO_NOTHING)
    remembrance_credit = models.IntegerField(default=40)
    applied_knowledge_credit = models.IntegerField(default=30)
    understanding_credit = models.IntegerField(default=30)
    subject_credit = models.IntegerField(default=100)

    class Meta:
        managed = True
        db_table = 'tblsubject'

    def __str__(self):
        return f'{self.subject_name} : {self.standard}'
