from django.db import models

from aagam_packages.django_model_extensions import models as amdl

from MySchoolHome.models import MySchoolUser


# TODO: Cascade Delete

# Create your models here.

class SubjectsManager(models.Manager):

    def create_subject(self, subject_name, std, r_credit, ak_credit, u_credit, s_credit):
        subject = self.model(subject_name=subject_name, standard=std, remembrance_credit=r_credit,
                             applied_knowledge_credit=ak_credit, understanding_credit=u_credit,
                             subject_credit=s_credit)
        subject.save()
        return subject

    def create_chapter(self, subject, ch_id, ch_name, ch_r_credit, ch_ak_credit, ch_u_credit, ch_credit):
        chapter = self.model(subject=subject, chapter_id=ch_id, chapter_name=ch_name, remembrance_credit=ch_r_credit,
                             applied_knowledge_credit=ch_ak_credit, understanding_credit=ch_u_credit,
                             chapter_credit=ch_credit)
        chapter.save()
        return chapter

    def create_topic(self, chapter, t_id, t_name):
        topic = self.model(subject_chapter=chapter, topic_id=t_id, topic_name=t_name)
        topic.save()
        return topic

    def delete_subject(self, subject_name, std):
        subject = self.model.objects.get(standard=std, subject_name=subject_name)
        subject.delete()
        return subject

    def delete_chapter(self, chapter_name, sub):
        chapter = self.model.objects.get(subject=sub, chapter_name=chapter_name)
        chapter.delete()
        return chapter

    def delete_topic(self, topic_name, chap):
        topic = self.model.objects.get(subject_chapter=chap, topic_name=topic_name)
        topic.delete()
        return topic

    def update_subject(self, s_id, subject_name, std, r_credit, ak_credit, u_credit, s_credit):
        subject = self.model.objects.get(subject_id=s_id)
        subject.subject_name = subject_name
        subject.standard = std
        subject.remembrance_credit = r_credit
        subject.applied_knowledge_credit = ak_credit
        subject.understanding_credit = u_credit
        subject.subject_credit = s_credit
        subject.save()
        return subject

    def update_chapter(self, s_c_id, ch_id, ch_name, ch_r_credit, ch_ak_credit, ch_u_credit, ch_credit):
        chapter = self.model.objects.get(subject_chapter_id=s_c_id)
        chapter.chapter_id = ch_id
        chapter.chapter_name = ch_name
        chapter.remembrance_credit = ch_r_credit
        chapter.applied_knowledge_credit = ch_ak_credit
        chapter.understanding_credit = ch_u_credit
        chapter.subject_credit = ch_credit
        chapter.save()
        return chapter

    def update_topic(self, c_t_id, t_id, t_name):
        topic = self.model.objects.get(chapter_topic_id=c_t_id)
        topic.topic_id = t_id
        topic.topic_name = t_name
        topic.save()
        return topic


class MapMySchoolUserSubject(amdl.AagamBaseModel):
    map_myschool_user_subject_id = models.AutoField(primary_key=True)
    myschool_user = models.ForeignKey(MySchoolUser, models.DO_NOTHING)
    subject = models.ForeignKey('TblSubject', models.DO_NOTHING)

    class Meta:
        db_table = 'map_myschool_user_subject'

    def __str__(self):
        return f'{self.subject} {self.myschool_user}'


class TblSubject(amdl.AagamBaseModel):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=20)
    standard = models.ForeignKey('Standard', models.DO_NOTHING)
    remembrance_credit = models.IntegerField(default=40)
    applied_knowledge_credit = models.IntegerField(default=30)
    understanding_credit = models.IntegerField(default=30)
    subject_credit = models.IntegerField(default=100)

    objects = SubjectsManager()

    class Meta:
        db_table = 'tblsubject'

    def __str__(self):
        return f'{self.subject_name} : {self.standard}'


class SubjectChapter(amdl.AagamBaseModel):
    subject_chapter_id = models.AutoField(primary_key=True)
    subject = models.ForeignKey('TblSubject', models.CASCADE)
    chapter_id = models.IntegerField()
    chapter_name = models.CharField(max_length=150)
    remembrance_credit = models.IntegerField()
    applied_knowledge_credit = models.IntegerField()
    understanding_credit = models.IntegerField()
    chapter_credit = models.IntegerField()

    objects = SubjectsManager()

    class Meta:
        db_table = 'subject_chapter'

    def __str__(self):
        return f'{self.chapter_id} {self.chapter_name} : {self.subject}'


class ChapterTopic(amdl.AagamBaseModel):
    chapter_topic_id = models.AutoField(primary_key=True)
    subject_chapter = models.ForeignKey('SubjectChapter', models.CASCADE)
    topic_id = models.IntegerField()
    topic_name = models.CharField(max_length=100)

    objects = SubjectsManager()

    class Meta:
        db_table = 'chapter_topic'

    def __str__(self):
        return f'{self.topic_id}. {self.topic_name} : {self.subject_chapter}'


class Standard(amdl.AagamBaseModel):
    standard = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'standard'

    def __str__(self):
        return str(self.standard)


class StandardSection(amdl.AagamBaseModel):
    standard_section_id = models.AutoField(primary_key=True)
    standard = models.ForeignKey(Standard, models.DO_NOTHING)
    section = models.CharField(max_length=1)

    class Meta:
        db_table = 'standard_section'

    def __str__(self):
        return f'{self.standard} {self.section}'


class MapMySchoolUserStandardSection(amdl.AagamBaseModel):
    map_my_school_user_standard_section = models.AutoField(primary_key=True)
    myschool_user = models.ForeignKey(MySchoolUser, models.DO_NOTHING)
    standard_section = models.ForeignKey(StandardSection, models.DO_NOTHING)

    class Meta:
        db_table = "map_myschool_user_standard_section"

    def __str__(self):
        return f'{self.standard_section} {self.myschool_user}'


class PaperType(amdl.AagamBaseModel):
    paper_type_id = models.AutoField(primary_key=True)
    paper_type = models.CharField(max_length=100)
    out_of = models.IntegerField()

    class Meta:
        db_table = 'paper_type'

    def __str__(self):
        return self.paper_type


class PaperEntry(amdl.AagamBaseModel):
    paper_entry_id = models.AutoField(primary_key=True)
    paper_entry_name = models.CharField(max_length=100)
    paper_type = models.ForeignKey('PaperType', models.CASCADE)
    paper_entry_status = models.BooleanField(default=True)
    paper_entry_date = models.DateField()

    class Meta:
        db_table = 'paper_entry'

    def __str__(self):
        return f'{self.paper_entry_name} : {self.paper_entry_date}'


class MapPaperEntrySubjectChapter(amdl.AagamBaseModel):
    map_paper_entry_subject_chapter = models.AutoField(primary_key=True)
    paper_entry = models.ForeignKey('PaperEntry', models.DO_NOTHING)
    subject_chapter = models.ForeignKey('SubjectChapter', models.DO_NOTHING)

    class Meta:
        db_table = 'map_paper_entry_subject_chapter'

    def __str__(self):
        return f'{self.subject_chapter} : {self.paper_entry}'


class PaperQuestion(amdl.AagamBaseModel):
    paper_question_id = models.AutoField(primary_key=True)
    paper_question_text = models.TextField()
    rau = (('R', 'Remembrance'), ('A', 'Application'), ('U', 'Understanding'))
    rau_type = models.CharField(max_length=1, choices=rau)
    total_marks = models.IntegerField()
    chapter_topic = models.ForeignKey('ChapterTopic', models.DO_NOTHING)

    class Meta:
        db_table = 'paper_question'

    def __str__(self):
        return f'{self.rau_type} : {self.chapter_topic} : {self.paper_question_text}'


class PaperPatternEntry(amdl.AagamBaseModel):
    paper_pattern_entry_id = models.AutoField(primary_key=True)
    paper_entry = models.ForeignKey('PaperEntry', models.DO_NOTHING)
    paper_question = models.ForeignKey('PaperQuestion', models.DO_NOTHING)

    class Meta:
        db_table = "paper_pattern_entry"

    def __str__(self):
        return f'{self.paper_entry} : {self.paper_question}'


class MapStudentPaperPatternEntry(amdl.AagamBaseModel):
    map_student_paper_pattern_entry_id = models.AutoField(primary_key=True)
    myschool_user = models.ForeignKey(MySchoolUser, models.DO_NOTHING)
    paper_pattern_entry = models.ForeignKey('PaperPatternEntry', models.DO_NOTHING)
    marks_obtained = models.IntegerField()  # TODO: Validation PaperQuestion totalmarks <= this

    class Meta:
        db_table = "map_myschool_user_paper_pattern_entry"

    def __str__(self):
        return f'{self.myschool_user} : {self.paper_pattern_entry}'

'''select paper_entry_name,marks_obtained,out_of,rau_type,total_marks from myschool_user as u inner join 
map_myschool_user_paper_pattern_entry as map on u.myschool_user_id = map.map_student_paper_pattern_entry_id 
inner join paper_pattern_entry as pp on map_student_paper_pattern_entry_id = pp.paper_pattern_entry_id 
inner join paper_question as pq on pp.paper_pattern_entry_id = pq.paper_question_id inner join 
paper_entry as pe on pp.paper_pattern_entry_id = pe.paper_entry_id inner join paper_type as pt on 
pe.paper_entry_id = pt.paper_type_id where paper_entry_name like '%mid%' and u.myschool_user_id=2;
'''