from django.shortcuts import render, HttpResponse
# Create your views here.
from .models import *
from django.db import connection
from django.db.models import Sum, Max, Min, Q, Avg
from MySchoolHome import views as mshv
from StudentPerformance import models as sp


def subject_entry(request):
    if request.method == "POST":
        sub_name = request.POST['sub_name']
        std = request.POST['std']
        r_credit = request.POST['r_credit']
        ak_credit = request.POST['ak_credit']
        u_credit = request.POST['u_credit']
        s_credit = request.POST['s_credit']

        try:
            std = Standard.objects.get(standard=std)
            subject = TblSubject.objects.create_subject(subject_name=sub_name, std=std, r_credit=r_credit,
                                                        ak_credit=ak_credit, u_credit=u_credit, s_credit=s_credit)

        except:
            print('Some Error occured')
        return render(request, 'entry.html')
    else:
        return render(request, 'entry.html')


def chapter_entry(request):
    if request.method == "POST":
        sub = request.POST['subject']
        chap_id = request.POST['ch_id']
        chap_name = request.POST['ch_name']
        ch_r_credit = request.POST['ch_r_credit']
        ch_ak_credit = request.POST['ch_ak_credit']
        ch_u_credit = request.POST['ch_u_credit']
        ch_credit = request.POST['ch_credit']

        try:
            sub = TblSubject.objects.get(subject_name=sub)
            chapter = SubjectChapter.objects.create_chapter(subject=sub, ch_id=chap_id, ch_name=chap_name,
                                                            ch_r_credit=ch_r_credit,
                                                            ch_ak_credit=ch_ak_credit, ch_u_credit=ch_u_credit,
                                                            ch_credit=ch_credit)
        except:
            print('Some Error occured')
        return render(request, 'entry.html')
    else:
        return render(request, 'entry.html')


def topic_entry(request):
    if request.method == "POST":
        chap = request.POST['chapter']
        t_id = request.POST['t_id']
        t_name = request.POST['t_name']

        try:
            chap = SubjectChapter.objects.get(chapter_name=chap)
            topic = ChapterTopic.objects.create_topic(Subject_chapter=chap, topic_id=t_id, topic_name=t_name)
        except:
            print("Some error !!!")
        return render(request, 'entry.html')
    else:
        return render(request, 'entry.html')


def subject_delete(request):
    if request.method == "POST":
        sub_name = request.POST['sub_name']
        std = request.POST['std']

        try:
            std = Standard.objects.get(standard=std)
            subject = TblSubject.objects.delete_subject(subject_name=sub_name, std=std)
        except:
            print('Some Error occurred')
        return render(request, 'entry.html')
    else:
        return render(request, 'entry.html')


def chapter_delete(request):
    if request.method == "POST":
        chap_name = request.POST['chap_name']
        sub = request.POST['sub']

        try:
            sub = TblSubject.objects.get(subject_name=sub)
            chapter = SubjectChapter.objects.delete_chapter(chapter_name=chap_name, sub=sub)
        except:
            print('Some Error occurred')
        return render(request, 'entry.html')
    else:
        return render(request, 'entry.html')


def topic_delete(request):
    if request.method == 'POST':
        t_name = request.POST['topic_name']
        chap = request.POST['chap']

        try:
            chap = SubjectChapter.objects.get(chapter_name=chap)
            topic = ChapterTopic.objects.delete_topic(topic_name=t_name, chap=chap)
        except:
            print('Some Error occurred')
        return render(request, 'entry.html')
    else:
        return render(request, 'entry.html')


def subject_update(request):
    if request.method == "POST":
        sub_id = request.POST['sub_id']
        sub_name = request.POST['sub_name']
        std = request.POST['std']
        r_credit = request.POST['r_credit']
        ak_credit = request.POST['ak_credit']
        u_credit = request.POST['u_credit']
        s_credit = request.POST['s_credit']

        try:
            std = Standard.objects.get(standard=std)
            subject = TblSubject.objects.update_subject(s_id=sub_id, subject_name=sub_name, std=std, r_credit=r_credit,
                                                        ak_credit=ak_credit, u_credit=u_credit, s_credit=s_credit)

        except:
            print('Some Error occured')
        return render(request, 'entry.html')
    else:
        return render(request, 'entry.html')


def chapter_update(request):
    if request.method == "POST":
        s_c_id = request.POST['s_c_id']
        ch_id = request.POST['ch_id']
        ch_name = request.POST['ch_name']
        ch_r_credit = request.POST['ch_r_credit']
        ch_ak_credit = request.POST['ch_ak_credit']
        ch_u_credit = request.POST['ch_u_credit']
        ch_credit = request.POST['ch_credit']

        try:
            chap = SubjectChapter.objects.update_chapter(s_c_id=s_c_id, ch_id=ch_id, ch_name=ch_name,
                                                         ch_r_credit=ch_r_credit, ch_ak_credit=ch_ak_credit,
                                                         ch_u_credit=ch_u_credit, ch_credit=ch_credit)

        except:
            print("Error occurred !!")
        return render(request, 'entry.html')
    else:
        return render(request, 'entry.html')


def topic_update(request):
    if request.method == "POST":
        c_t_id = request.POST['c_t_id']
        t_id = request.POST['t_id']
        t_name = request.POST['t_name']

        try:
            topic = ChapterTopic.objects.update_topic(c_t_id=c_t_id, t_id=t_id, t_name=t_name)

        except:
            print('Some Error occurred')
        return render(request, 'entry.html')
    else:
        return render(request, 'entry.html')


def total_mid(request):
    cursor = connection.cursor()
    cursor.execute(
        ''' SELECT sum(marks_obtained), sum(total_marks) FROM map_myschool_user_paper_pattern_entry as m, paper_pattern_entry as a,myschool_user as b, paper_question as c, paper_entry as d, paper_type as t where m.paper_pattern_entry_id=a.paper_pattern_entry_id AND m.myschool_user_id=13 and paper_type = "mid_exam" ''')
    mid_marks = cursor.fetchall()
    return mid_marks
    # m = MapStudentPaperPatternEntry.objects.filter(myschool_user=13).select_related('paper_pattern_entry').select_related('paper_pattern_entry__paper_question')
    # SELECT sum(marks_obtained), sum(c.total_marks) FROM map_myschool_user_paper_pattern_entry as m, paper_pattern_entry as a,myschool_user as b, paper_question as c WHERE m.paper_pattern_entry_id=a.paper_pattern_entry_id AND m.myschool_user_id=13;


def total_final(request):
    cursor = connection.cursor()
    cursor.execute(
        ''' SELECT sum(total_marks), sum(marks_obtained) FROM map_myschool_user_paper_pattern_entry as m, paper_pattern_entry as a,myschool_user as b, paper_question as c, paper_entry as d, paper_type as t where m.paper_pattern_entry_id=a.paper_pattern_entry_id AND m.myschool_user_id=13 and paper_type = "final_exam" ''')
    final_marks = cursor.fetchall()
    return final_marks


def rau_mid(request):
    cursor = connection.cursor()
    cursor.execute(''' ''')
    mid_rau = cursor.fetchall()
    return mid_rau

def student_dashboard(request):
    if request.user.groups.filter(name='Learner').exists():

        stud = sp.MapStudentPaperPatternEntry.objects.all().filter(myschool_user=13).select_related('paper_pattern_entry')

        r_s = stud.filter(paper_pattern_entry__paper_question__rau_type='R').aggregate(Avg('marks_obtained'))
        a_s = stud.filter(paper_pattern_entry__paper_question__rau_type='A').aggregate(Avg('marks_obtained'))
        u_s = stud.filter(paper_pattern_entry__paper_question__rau_type='U').aggregate(Avg('marks_obtained'))

        subjects = stud.values_list(
            'paper_pattern_entry__paper_question__chapter_topic__subject_chapter__subject__subject_name',
            flat=True).distinct()

        for i in range(len(subjects)):
            marks = (subjects.filter(
                paper_pattern_entry__paper_question__chapter_topic__subject_chapter__subject__subject_name=subjects[i]))\
            .aggregate(Avg('marks_obtained'))

        ass = stud.filter(
            paper_pattern_entry__paper_entry__paper_type__paper_type='Assignment').aggregate(Avg('marks_obtained'))
        pra = stud.filter(
            paper_pattern_entry__paper_entry__paper_type__paper_type='Practical').aggregate(Avg('marks_obtained'))
        uni = stud.filter(
            paper_pattern_entry__paper_entry__paper_type__paper_type='Unit').aggregate(Avg('marks_obtained'))
        mid = stud.filter(
            paper_pattern_entry__paper_entry__paper_type__paper_type='Mid').aggregate(Avg('marks_obtained'))
        fin = stud.filter(
            paper_pattern_entry__paper_entry__paper_type__paper_type='Final').aggregate(Avg('marks_obtained'))
        pass
    else:
        pass

def performance_formative(request, **kwargs):
    if request.user.groups.filter(name='Learner').exists():
        a = sp.MapStudentPaperPatternEntry.objects.select_related('paper_pattern_entry') \
            .filter(myschool_user=13).exclude(Q(paper_pattern_entry__paper_entry__paper_type__paper_type__icontains='mid')
                                              & Q(paper_pattern_entry__paper_entry__paper_type__paper_type__icontains='final'))
        subjects = a.values_list(
            'paper_pattern_entry__paper_question__chapter_topic__subject_chapter__subject__subject_name',
            flat=True).distinct()
        ass = a.filter(paper_pattern_entry__paper_entry__paper_type__paper_type='assignment')
        assign = ass.aggregate(Avg('marks_obtained'))
        pra = a.filter(paper_pattern_entry__paper_entry__paper_type__paper_type='practical')
        prac = pra.aggregate(Avg('marks_obtained'))
        un = a.filter(paper_pattern_entry__paper_entry__paper_type__paper_type='unit')
        uni = un.aggregate(Avg('marks_obtained'))

        ##################################################################################################################

        #############################   R A U Graph    ###################################################################

        chapter = subjects.values_list('paper_pattern_entry__paper_question__chapter_topic__subject_chapter__chapter_name', flat=True).distinct()

        for i in range(len(subjects)):
            rm = chapter.filter(
                paper_pattern_entry__paper_question__chapter_topic__subject_chapter__subject__subject_name=subjects[i],
                paper_pattern_entry__paper_question__rau_type='R')
            r = rm.aggregate(Avg('marks_obtained'))
            am = chapter.filter(
                paper_pattern_entry__paper_question__chapter_topic__subject_chapter__subject__subject_name=subjects[i],
                paper_pattern_entry__paper_question__rau_type='R')
            aa = am.aggregate(Avg('marks_obtained'))
            um = chapter.filter(
                paper_pattern_entry__paper_question__chapter_topic__subject_chapter__subject__subject_name=subjects[i],
                paper_pattern_entry__paper_question__rau_type='R')
            u = um.aggregate(Avg('marks_obtained'))

        pass
    else:
        pass


def performance_mid(request, **kwargs):
    if request.user.groups.filter(name='Learner').exists():
        student_navbar = mshv.student_navbar(request)
        stud_id = sp.MapStudentPaperPatternEntry.objects. \
            select_related('myschool_user', 'auth_user') \
            .filter(myschool_user_id=13).values('myschool_user__auth_user__username')
        standard = request.GET.get('standard', student_navbar['standard'].first()['subject__standard'])
        section = request.GET.get('section', student_navbar['section'].first()['section'])
        subject = request.GET.get('subject', student_navbar['subject'].first()['subject'])

        a = sp.MapStudentPaperPatternEntry.objects.select_related('paper_pattern_entry') \
            .filter(myschool_user=13, paper_pattern_entry__paper_entry__paper_type__paper_type__contains="mid")

        # .values('marks_obtained',
        # 'paper_pattern_entry__paper_question__chapter_topic__subject_chapter__subject__subject_name',
        # \ 'paper_pattern_entry__paper_entry__paper_type__paper_type',
        # 'paper_pattern_entry__paper_question__paper_question_text')

        #############################   MID Performance Graph    ######################################

        # subjects = a.values_list(
        # 'paper_pattern_entry__paper_question__chapter_topic__subject_chapter__subject__subject_name',
        # flat=True).distinct()

        # for i in range(len(subjects)):
        # ...     print(subjects[i])

        # for i in range(len(subjects)):
        #     a = list(subjects.values_list('marks_obtained', flat=True))
        #     k = sum(a)
        #     print(k)

        s = sp.MapStudentPaperPatternEntry.objects.select_related('paper_pattern_entry') \
            .filter(paper_pattern_entry__paper_entry__paper_type__paper_type__contains="mid")

        ma = s.aggregate(Max('marks_obtained'))
        mi = s.aggregate(Min('marks_obtained'))

        ######################################################################################################################

        #############################   MID R A U Graph    ###################################################################

        subjects = a.values_list(
            'paper_pattern_entry__paper_question__chapter_topic__subject_chapter__subject__subject_name',
            flat=True).distinct()

        # for i in range(len(subjects)):
        # ...     print(subjects[i])

        for i in range(len(subjects)):
            r = subjects.filter(paper_pattern_entry__paper_question__rau_type='R')
            rm = list(r.values_list('marks_obtained', flat=True))
            rk = sum(rm)
            a = subjects.filter(paper_pattern_entry__paper_question__rau_type='A')
            am = list(a.values_list('marks_obtained', flat=True))
            ak = sum(am)
            u = subjects.filter(paper_pattern_entry__paper_question__rau_type='U')
            um = list(u.values_list('marks_obtained', flat=True))
            uk = sum(um)
            print(subjects[i])
            print(rk)
            print(ak)
            print(uk)

        ######################################################################################################################

        #############################   MID MARKS TABLE    ###################################################################

        ab = a.filter(
            paper_pattern_entry__paper_question__chapter_topic__subject_chapter__subject__subject_name="Mathematics 9709")

        sub = ab.values_list(
            'paper_pattern_entry__paper_question__chapter_topic__subject_chapter__subject__subject_name',
            flat=True).distinct()

        rr = ab.filter(paper_pattern_entry__paper_question__rau_type='R')
        rm = list(rr.values_list('marks_obtained', flat=True))
        r_mark = sum(rm)

        aa = ab.filter(paper_pattern_entry__paper_question__rau_type='A')
        am = list(aa.values_list('marks_obtained', flat=True))
        a_mark = sum(am)

        uu = ab.filter(paper_pattern_entry__paper_question__rau_type='U')
        um = list(uu.values_list('marks_obtained', flat=True))
        u_mark = sum(um)

        total_mid = ab.aggregate(Sum('paper_pattern_entry__paper_question__total_marks'))

        obtained_mid = ab.aggregate(Sum('marks_obtained'))

        ######################################################################################################################

        # cursor = connection.cursor()
        # cursor.execute(
        #     ''' SELECT sum(marks_obtained), sum(total_marks) FROM map_myschool_user_paper_pattern_entry as m, paper_pattern_entry as a,myschool_user as b, paper_question as c, paper_entry as d, paper_type as t where m.paper_pattern_entry_id=a.paper_pattern_entry_id AND m.myschool_user_id=13 and paper_type = "mid_exam" ''')
        # mid_total_marks = cursor.fetchall()

    else:
        return HttpResponse("<h1>Educator |!| Principal</h1>")


def performance_final(request, **kwargs):
    if request.user.groups.filter(name='Learner').exists():
        student_navbar = mshv.student_navbar(request)
        stud_id = sp.MapStudentPaperPatternEntry.objects. \
            select_related('myschool_user', 'auth_user') \
            .filter(myschool_user_id=18).values('myschool_user__auth_user__username')
        standard = request.GET.get('standard', student_navbar['standard'].first()['subject__standard'])
        section = request.GET.get('section', student_navbar['section'].first()['section'])
        subject = request.GET.get('subject', student_navbar['subject'].first()['subject'])

        a = sp.MapStudentPaperPatternEntry.objects.select_related('paper_pattern_entry') \
            .filter(myschool_user=13, paper_pattern_entry__paper_entry__paper_type__paper_type__contains="final")

        # .values('marks_obtained', 'paper_pattern_entry__paper_question__chapter_topic__subject_chapter__subject__subject_name', \
        # 'paper_pattern_entry__paper_entry__paper_type__paper_type', 'paper_pattern_entry__paper_question__paper_question_text')

        #############################   MID Performance Graph    ###################################################################

        # subjects = a.values_list('paper_pattern_entry__paper_question__chapter_topic__subject_chapter__subject__subject_name', flat=True).distinct()

        # for i in range(len(subjects)):
        # ...     print(subjects[i])

        # for i in range(len(subjects)):
        #     a = list(subjects.values_list('marks_obtained', flat=True))
        #     k = sum(a)
        #     print(k)

        s = sp.MapStudentPaperPatternEntry.objects.select_related('paper_pattern_entry') \
            .filter(paper_pattern_entry__paper_entry__paper_type__paper_type__contains="mid")

        ma = s.aggregate(Max('marks_obtained'))
        mi = s.aggregate(Min('marks_obtained'))

        ######################################################################################################################

        #############################   MID R A U Graph    ###################################################################

        subjects = a.values_list(
            'paper_pattern_entry__paper_question__chapter_topic__subject_chapter__subject__subject_name',
            flat=True).distinct()

        # for i in range(len(subjects)):
        # ...     print(subjects[i])

        for i in range(len(subjects)):
            r = subjects.filter(paper_pattern_entry__paper_question__rau_type='R')
            rm = list(r.values_list('marks_obtained', flat=True))
            rk = sum(rm)
            a = subjects.filter(paper_pattern_entry__paper_question__rau_type='A')
            am = list(a.values_list('marks_obtained', flat=True))
            ak = sum(am)
            u = subjects.filter(paper_pattern_entry__paper_question__rau_type='U')
            um = list(u.values_list('marks_obtained', flat=True))
            uk = sum(um)
            print(subjects[i])
            print(rk)
            print(ak)
            print(uk)

        ######################################################################################################################

        #############################   MID MARKS TABLE    ###################################################################

        ab = a.filter(
            paper_pattern_entry__paper_question__chapter_topic__subject_chapter__subject__subject_name="Mathematics 9709")

        sub = ab.values_list(
            'paper_pattern_entry__paper_question__chapter_topic__subject_chapter__subject__subject_name',
            flat=True).distinct()

        rr = ab.filter(paper_pattern_entry__paper_question__rau_type='R')
        rm = list(rr.values_list('marks_obtained', flat=True))
        r_mark = sum(rm)

        aa = ab.filter(paper_pattern_entry__paper_question__rau_type='A')
        am = list(aa.values_list('marks_obtained', flat=True))
        a_mark = sum(am)

        uu = ab.filter(paper_pattern_entry__paper_question__rau_type='U')
        um = list(uu.values_list('marks_obtained', flat=True))
        u_mark = sum(um)

        total_mid = ab.aggregate(Sum('paper_pattern_entry__paper_question__total_marks'))

        obtained_mid = ab.aggregate(Sum('marks_obtained'))

        ######################################################################################################################

        # cursor = connection.cursor()
        # cursor.execute(
        #     ''' SELECT sum(marks_obtained), sum(total_marks) FROM map_myschool_user_paper_pattern_entry as m, paper_pattern_entry as a,myschool_user as b, paper_question as c, paper_entry as d, paper_type as t where m.paper_pattern_entry_id=a.paper_pattern_entry_id AND m.myschool_user_id=13 and paper_type = "mid_exam" ''')
        # mid_total_marks = cursor.fetchall()

    else:
        return HttpResponse("<h1>Educator |!| Principal</h1>")
