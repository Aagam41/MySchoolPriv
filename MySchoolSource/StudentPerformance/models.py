from django.db import models

from aagam_packages.django.model_extensions import models as amdl

from MySchoolHome.models import MySchoolUser


# region Aagam Sheth
class TblSubject(amdl.AagamBaseModel):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=20)
    standard = models.ForeignKey('TblStandard', models.DO_NOTHING)
    remembrance_credit = models.IntegerField(default=40)
    applied_knowledge_credit = models.IntegerField(default=30)
    understanding_credit = models.IntegerField(default=30)
    subject_credit = models.IntegerField(default=100)

    class Meta:
        db_table = 'tblsubject'

    def __str__(self):
        return f'{self.subject_name}'


class SubjectChapter(amdl.AagamBaseModel):
    subject_chapter_id = models.AutoField(primary_key=True)
    subject = models.ForeignKey('TblSubject', on_delete=models.CASCADE)
    chapter_id = models.IntegerField()
    chapter_name = models.CharField(max_length=150)
    remembrance_credit = models.IntegerField()
    applied_knowledge_credit = models.IntegerField()
    understanding_credit = models.IntegerField()
    chapter_credit = models.IntegerField()

    class Meta:
        db_table = 'subject_chapter'

    def __str__(self):
        return f'{self.chapter_id} {self.chapter_name} : {self.subject}'


class ChapterTopic(amdl.AagamBaseModel):
    chapter_topic_id = models.AutoField(primary_key=True)
    subject_chapter = models.ForeignKey('SubjectChapter', models.DO_NOTHING)
    topic_id = models.IntegerField()
    topic_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'chapter_topic'

    def __str__(self):
        return f'{self.topic_id}. {self.topic_name} : {self.subject_chapter}'


class TblStandard(amdl.AagamBaseModel):
    standard = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'tblstandard'

    def __str__(self):
        return str(self.standard)


class MapMySchoolUserStandardSection(amdl.AagamBaseModel):
    map_my_school_user_standard_section_id = models.AutoField(primary_key=True)
    myschool_user = models.ForeignKey(MySchoolUser, models.DO_NOTHING)
    standard = models.ForeignKey(TblStandard, models.DO_NOTHING)
    section = models.CharField(max_length=1)
    status = models.BooleanField()

    class Meta:
        db_table = "map_myschool_user_standard_section"

    def __str__(self):
        return f'{self.standard} {self.myschool_user}'


class MapMySchoolUserSubject(amdl.AagamBaseModel):
    map_myschool_user_subject_id = models.AutoField(primary_key=True)
    myschool_user = models.ForeignKey(MySchoolUser, models.DO_NOTHING)
    subject = models.ForeignKey('TblSubject', models.DO_NOTHING)
    status = models.BooleanField()

    class Meta:
        db_table = 'map_myschool_user_subject'

    def __str__(self):
        return f'{self.subject} {self.myschool_user}'


class PaperType(amdl.AagamBaseModel):
    paper_type_id = models.AutoField(primary_key=True)
    paper_type = models.CharField(max_length=100)
    assessment_type = models.BooleanField(default=True, help_text="True if is Formative else False")
    out_of = models.IntegerField()

    class Meta:
        db_table = 'paper_type'

    def __str__(self):
        return self.paper_type


class PaperEntry(amdl.AagamBaseModel):
    paper_entry_id = models.AutoField(primary_key=True)
    paper_entry_name = models.CharField(max_length=100)
    subject = models.ForeignKey('TblSubject', models.DO_NOTHING)
    paper_type = models.ForeignKey('PaperType', models.DO_NOTHING)
    paper_entry_status = models.BooleanField(default=True)
    paper_entry_date = models.DateField()

    class Meta:
        db_table = 'paper_entry'

    def __str__(self):
        return f'{self.paper_entry_name} : {self.subject} : {self.paper_entry_date}'


class PaperPatternEntry(amdl.AagamBaseModel):
    paper_pattern_entry_id = models.AutoField(primary_key=True)
    paper_entry = models.ForeignKey('PaperEntry', models.DO_NOTHING)
    paper_question_id = models.IntegerField()
    rau = (('R', 'Remembrance'), ('A', 'Application'), ('U', 'Understanding'))
    rau_type = models.CharField(max_length=1, choices=rau)
    total_marks = models.IntegerField()
    chapter_topic = models.ForeignKey('ChapterTopic', models.DO_NOTHING)

    class Meta:
        db_table = "paper_pattern_entry"

    def __str__(self):
        return f'{self.paper_entry}'


class MapStudentPaperPatternEntry(amdl.AagamBaseModel):
    map_student_paper_pattern_entry_id = models.AutoField(primary_key=True)
    map_myschool_user_standard_section = models.ForeignKey(MapMySchoolUserStandardSection, models.DO_NOTHING)
    paper_pattern_entry = models.ForeignKey('PaperPatternEntry', models.DO_NOTHING)
    marks_obtained = models.IntegerField()  # TODO: Validation PaperQuestion totalmarks <= this

    class Meta:
        db_table = "map_myschool_user_paper_pattern_entry"

    def __str__(self):
        return f'{self.paper_pattern_entry}'
# endregion
