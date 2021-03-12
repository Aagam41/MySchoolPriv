from django.db.models import Sum, Max, Min, Q, Avg
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from MySchoolHome import models as msh
from MySchoolHome import views as mshv
from StudentPerformance import models as sp
from aagam_packages.terminal_yoda.terminal_yoda import *


# region Aagam Sheth
def performance_panel(request, **kwargs):
    if request.user.groups.filter(name='Learner').exists():
        navbar = mshv.student_navbar(request)
        user = "learner"

        context = {
            'performance_type': kwargs.get('performance_type'),
            'navbar': navbar,
            'user_group': user,
        }

        if kwargs.get('performance_type') == "Formative":
            return render(request, 'StudentPerformance/formative.html', context)
        elif kwargs.get('performance_type') == "Summative":
            return render(request, 'StudentPerformance/summative.html', context)

    elif request.user.groups.filter(name='Educator').exists():
        educator_context = mshv.educator_navbar(request)
        standard = request.GET.get('standard', educator_context['standard'].first()['subject__standard'])
        section = request.GET.get('section', educator_context['section'].first()['section'])
        subject = request.GET.get('tblsubject', educator_context['user_subject'].first().subject)

        learner = sp.MapMySchoolUserStandardSection.objects \
            .filter(standard=standard, section=section, status=True)
        learner_detail = msh.MySchoolUser.objects.filter(myschool_user_id__in=learner.values('myschool_user__pk'))

        graph = None
        rau = None

        if not kwargs.get('performance_type') == 'Prediction':
            graph = get_teacher_assessment_performer_level_count_graph(request,
                                                                       subject,
                                                                       learner,
                                                                       kwargs.get('performance_type'))
            if kwargs.get('performance_type') == 'Formative':
                rau = get_teacher_formative_chapter_wise_rau_count_graph(request, subject, learner,
                                                                         kwargs.get('performance_type'))
            elif kwargs.get('performance_type') == 'Summative':
                rau = get_teacher_summative_rau_count_graph(request, subject, learner, kwargs.get('performance_type'))
        user = "educator"

        context = {
            'learners': learner_detail,
            'graph': graph,
            'rau': rau,
            'performance_type': kwargs.get('performance_type'),
            'navbar': educator_context,
            'user_group': user,
        }
        if kwargs.get('performance_type') == "Formative":
            return render(request, 'StudentPerformance/formative.html', context)
        elif kwargs.get('performance_type') == "Summative":
            return render(request, 'StudentPerformance/summative.html', context)
        elif kwargs.get('performance_type') == "Prediction":
            return render(request, 'StudentPerformance/educator_panel_student_list.html', context)

    elif request.user.groups.filter(name='Principal').exists():
        navbar = mshv.principal_navbar()
        subject_educator = sp.MapMySchoolUserSubject.objects.filter(
            subject__standard=request.GET.get('standard', navbar['standard'].first().standard))
        map_id = sp.MapMySchoolUserStandardSection.objects \
            .filter(standard=request.GET.get('standard', navbar['standard'].first().standard),
                    section=request.GET.get('section', navbar['section'].first()['section']), status=True)
        subject = \
            sp.TblSubject.objects.filter(standard=request.GET.get('standard', navbar['standard'].first().standard))

        graph = dict()
        rau = dict()

        if not kwargs.get('performance_type') == 'Prediction':
            for sub in subject:
                graph[sub.subject_name] = get_teacher_assessment_performer_level_count_graph(request,
                                                                                             sub.subject_name,
                                                                                             map_id,
                                                                                             kwargs.get(
                                                                                                 'performance_type'))
                if kwargs.get('performance_type') == 'Formative':
                    rau[sub.subject_name] = \
                        get_teacher_formative_chapter_wise_rau_count_graph(request,
                                                                           sub.subject_name,
                                                                           map_id,
                                                                           kwargs.get('performance_type'))
                elif kwargs.get('performance_type') == 'Summative':
                    rau[sub.subject_name] = \
                        get_teacher_summative_rau_count_graph(request,
                                                              sub.subject_name,
                                                              map_id,
                                                              kwargs.get('performance_type'))
        user = "principal"
        context = {'page_context': {'title': "MySchool Principal Dashboard",
                                    'titleTag': 'MySchool'},
                   'performance_type': kwargs.get('performance_type'),
                   'subject_educators': subject_educator,
                   'learners': map_id,
                   'subject': subject,
                   'graph': graph,
                   'rau': rau,
                   'navbar': navbar,
                   'user_group': user, }
    if kwargs.get('performance_type') == "Formative":
        return render(request, 'StudentPerformance/formative.html', context)
    elif kwargs.get('performance_type') == "Summative":
        return render(request, 'StudentPerformance/summative.html', context)
    elif kwargs.get('performance_type') == "Prediction":
        return render(request, 'StudentPerformance/educator_panel_student_list.html', context)


def student_performance(request, **kwargs):
    if request.user.groups.filter(name='Educator').exists():
        educator_context = mshv.educator_navbar(request)
        standard = request.GET.get('standard', educator_context['standard'].first()['subject__standard'])
        section = request.GET.get('section', educator_context['section'].first()['section'])
        learner = sp.MapMySchoolUserStandardSection.objects \
            .filter(standard=standard, section=section, status=True) \
            .values_list("myschool_user__pk")
        learner_detail = msh.MySchoolUser.objects.filter(myschool_user_id__in=learner)

        passed = 0
        failed = 0
        rau = 0

        context = {
            'learners': learner_detail,
            'passed_students': passed,
            'failed_students': failed,
            'rau': rau,
            'performance_type': kwargs.get('performance_type'),
            'navbar': educator_context,
        }
        return render(request, 'StudentPerformance/educator_panel_student_list.html', context)
    elif request.user.groups.filter(name='Principal').exists():
        navbar = mshv.principal_navbar()
        subject_educator = sp.MapMySchoolUserSubject.objects.filter(
            subject__standard=request.GET.get('standard', navbar['standard'].first().standard))
        map_id = sp.MapMySchoolUserStandardSection.objects \
            .filter(standard=request.GET.get('standard', navbar['standard'].first().standard),
                    section=request.GET.get('section', navbar['section'].first()['section']), status=True)

        passed = 0
        failed = 0
        rau = 0

        context = {'page_context': {'title': "MySchool Principal Dashboard",
                                    'titleTag': 'MySchool'},
                   'performance_type': kwargs.get('performance_type'),
                   'subject_educators': subject_educator,
                   'learners': map_id,
                   'passed_students': passed,
                   'failed_students': failed,
                   'rau': rau,
                   'navbar': navbar,
                   }
        return render(request, 'StudentPerformance/principal_panel_teacher_student_list.html', context)


def get_performance_type(performance_type) -> bool:
    if performance_type == 'Formative':
        return True
    elif performance_type == 'Summative':
        return False
    else:
        raise AttributeError('performance_type should either be Formative or Summative')


def get_teacher_assessment_performer_level_count_graph(request, subject, learner, performance_type):
    total_marks_obtained = sp.MapStudentPaperPatternEntry.objects \
        .filter(map_myschool_user_standard_section__in=learner,
                paper_pattern_entry__paper_entry__subject__subject_name=subject,
                paper_pattern_entry__paper_entry__paper_type__assessment_type=get_performance_type(performance_type)) \
        .values('paper_pattern_entry__paper_entry', 'map_myschool_user_standard_section') \
        .order_by('map_myschool_user_standard_section', 'paper_pattern_entry__paper_entry', ) \
        .annotate(total_marks_obtained=Sum('marks_obtained'))

    paper_type = sp.PaperType.objects.filter(assessment_type=get_performance_type(performance_type))

    paper_wise_total_marks_obtained = dict()
    cutoff_marks = dict()
    top_count = dict()
    mid_count = dict()
    low_count = dict()

    for paper in paper_type:
        paper_wise_total_marks_obtained[paper.paper_type] = \
            total_marks_obtained.filter(
                paper_pattern_entry__paper_entry__paper_type=paper)

        cutoff_marks[paper.paper_type] = int((paper.out_of / 100) * 33)

        top_cutoff = (cutoff_marks[paper.paper_type] * 2) + (cutoff_marks[paper.paper_type] / 2)

        top_count[paper.paper_type] = paper_wise_total_marks_obtained[paper.paper_type] \
            .filter(total_marks_obtained__gte=top_cutoff).count()
        mid_count[paper.paper_type] = paper_wise_total_marks_obtained[paper.paper_type] \
            .filter(total_marks_obtained__lt=top_cutoff,
                    total_marks_obtained__gt=cutoff_marks[paper.paper_type]).count()
        low_count[paper.paper_type] = paper_wise_total_marks_obtained[paper.paper_type] \
            .filter(total_marks_obtained__lte=cutoff_marks[paper.paper_type]).count()

    context = {
        'paper_wise': paper_wise_total_marks_obtained,
        'cutoff_marks': cutoff_marks,
        'top_count': top_count,
        'mid_count': mid_count,
        'low_count': low_count,
    }

    return context


def get_teacher_formative_chapter_wise_rau_count_graph(request, subject, learner, performance_type):
    total_marks_obtained = sp.MapStudentPaperPatternEntry.objects.filter(
        map_myschool_user_standard_section__in=learner,
        paper_pattern_entry__paper_entry__subject__subject_name=subject,
        paper_pattern_entry__paper_entry__paper_type__assessment_type=get_performance_type(performance_type)
    ).values('paper_pattern_entry__paper_entry__subject__subject_name',
             'paper_pattern_entry__chapter_topic__subject_chapter',
             'paper_pattern_entry__rau_type') \
        .annotate(total_marks_obtained=Avg('marks_obtained'),
                  outoff_total_marks=Avg('paper_pattern_entry__total_marks'))

    yoda_saberize_print(total_marks_obtained)

    chapter_list = list()
    chapter_wise_r = dict()
    chapter_wise_a = dict()
    chapter_wise_u = dict()

    chapter_wise_r_list = list()
    chapter_wise_a_list = list()
    chapter_wise_u_list = list()

    for chapter in total_marks_obtained.values('paper_pattern_entry__chapter_topic__subject_chapter',
                                               'paper_pattern_entry__chapter_topic__subject_chapter__chapter_name') \
            .distinct():
        chapter_list.append(chapter['paper_pattern_entry__chapter_topic__subject_chapter__chapter_name'])

        chapter_wise_r[chapter_list[-1]] = total_marks_obtained.filter(
            paper_pattern_entry__chapter_topic__subject_chapter=
            chapter['paper_pattern_entry__chapter_topic__subject_chapter'],
            paper_pattern_entry__rau_type='R').values('paper_pattern_entry__rau_type') \
            .annotate(total_marks_obtained=Avg('marks_obtained'),
                      outoff_total_marks=Avg('paper_pattern_entry__total_marks'))

        chapter_wise_a[chapter_list[-1]] = total_marks_obtained.filter(
            paper_pattern_entry__chapter_topic__subject_chapter=
            chapter['paper_pattern_entry__chapter_topic__subject_chapter'],
            paper_pattern_entry__rau_type='A').values('paper_pattern_entry__rau_type') \
            .annotate(total_marks_obtained=Avg('marks_obtained'),
                      outoff_total_marks=Avg('paper_pattern_entry__total_marks'))

        chapter_wise_u[chapter_list[-1]] = total_marks_obtained.filter(
            paper_pattern_entry__chapter_topic__subject_chapter=
            chapter['paper_pattern_entry__chapter_topic__subject_chapter'],
            paper_pattern_entry__rau_type='U').values('paper_pattern_entry__rau_type') \
            .annotate(total_marks_obtained=Avg('marks_obtained'),
                      outoff_total_marks=Avg('paper_pattern_entry__total_marks'))

        yoda_saberize_print(chapter_wise_r, YodaSaberColor.RED)
        yoda_saberize_print(chapter_wise_a, YodaSaberColor.DARKGREEN)
        yoda_saberize_print(chapter_wise_u, YodaSaberColor.CADETBLUE)

        chapter_wise_r_list.append(int(((dict(chapter_wise_r[chapter_list[-1]][0])['total_marks_obtained']) /
                                        (dict(chapter_wise_r[chapter_list[-1]][0])['outoff_total_marks'])) * 100))
        chapter_wise_a_list.append(int(((dict(chapter_wise_a[chapter_list[-1]][0])['total_marks_obtained']) /
                                        (dict(chapter_wise_a[chapter_list[-1]][0])['outoff_total_marks'])) * 100))
        chapter_wise_u_list.append(int(((dict(chapter_wise_u[chapter_list[-1]][0])['total_marks_obtained']) /
                                        (dict(chapter_wise_u[chapter_list[-1]][0])['outoff_total_marks'])) * 100))

    yoda_saberize_print(chapter_wise_r_list, YodaSaberColor.DARKCYAN)
    yoda_saberize_print(chapter_wise_a_list, YodaSaberColor.LAVENDER)
    yoda_saberize_print(chapter_wise_u_list, YodaSaberColor.MEDIUMPURPLE)

    context = {
        'chapter_list': chapter_list,
        'chapter_wise_r': chapter_wise_r_list,
        'chapter_wise_a': chapter_wise_a_list,
        'chapter_wise_u': chapter_wise_u_list
    }

    return context


def get_teacher_summative_rau_count_graph(request, subject, learner, performance_type):
    total_marks_obtained = sp.MapStudentPaperPatternEntry.objects.filter(
        map_myschool_user_standard_section__in=learner,
        paper_pattern_entry__paper_entry__subject__subject_name=subject,
        paper_pattern_entry__paper_entry__paper_type__assessment_type=get_performance_type(performance_type)
    ).values('paper_pattern_entry__paper_entry__subject__subject_name',
             'paper_pattern_entry__rau_type') \
        .annotate(total_marks_obtained=Avg('marks_obtained'),
                  outoff_total_marks=Avg('paper_pattern_entry__total_marks'))

    yoda_saberize_print(total_marks_obtained)

    r = total_marks_obtained.filter(paper_pattern_entry__rau_type='R')
    a = total_marks_obtained.filter(paper_pattern_entry__rau_type='A')
    u = total_marks_obtained.filter(paper_pattern_entry__rau_type='U')

    rau = [(int(((dict(r[0])['total_marks_obtained']) /
                 (dict(r[0])['outoff_total_marks'])) * 100)),
           (int(((dict(a[0])['total_marks_obtained']) /
                 (dict(a[0])['outoff_total_marks'])) * 100)),
           (int(((dict(u[0])['total_marks_obtained']) /
                 (dict(u[0])['outoff_total_marks'])) * 100))
           ]

    return rau


# endregion


# region Yash
def get_performance_formative_grpah(request):
    navbar_context = mshv.student_navbar(request)
    current_my_school_user = sp.MapMySchoolUserStandardSection.objects.get(myschool_user__auth_user=request.user,
                                                                           section=
                                                                           navbar_context['standard_section_current'][
                                                                               'section'],
                                                                           standard=
                                                                           navbar_context['standard_section_current'][
                                                                               'standard'],
                                                                           status=True)
    a = sp.MapStudentPaperPatternEntry.objects.select_related('paper_pattern_entry') \
        .filter(map_myschool_user_standard_section=current_my_school_user).exclude(
        Q(paper_pattern_entry__paper_entry__paper_type__paper_type__icontains='mid')
        & Q(paper_pattern_entry__paper_entry__paper_type__paper_type__icontains='final'))
    yoda_saberize_print(a, YodaSaberColor.WHITE, YodaSaberColor.HOTPINK)
    subjects = a.values_list(
        'paper_pattern_entry__chapter_topic__subject_chapter__subject__subject_name',
        flat=True).distinct()

    ass = a.filter(paper_pattern_entry__paper_entry__paper_type__paper_type='assignment')
    assign = ass.aggregate(Avg('marks_obtained'))
    pra = a.filter(paper_pattern_entry__paper_entry__paper_type__paper_type='practical')
    prac = pra.aggregate(Avg('marks_obtained'))
    un = a.filter(paper_pattern_entry__paper_entry__paper_type__paper_type='unit')
    uni = un.aggregate(Avg('marks_obtained'))

    subject_assignment = ass

    for sub in subjects:
        subject_assignment = ass.filter(paper_pattern_entry__chapter_topic__subject_chapter__subject__subject_name=sub)
        yoda_saberize_print(subject_assignment, YodaSaberColor.WHITE, YodaSaberColor.HOTPINK)

        ass = subject_assignment.filter(paper_pattern_entry__paper_entry__paper_type__paper_type='assignment')
        assign = ass.aggregate(Avg('marks_obtained'))
        pra = subject_assignment.filter(paper_pattern_entry__paper_entry__paper_type__paper_type='practical')
        prac = pra.aggregate(Avg('marks_obtained'))
        un = a.filter(paper_pattern_entry__paper_entry__paper_type__paper_type='unit')
        uni = un.aggregate(Avg('marks_obtained'))
        pass

    #############################   R A U Graph    ###################################################################
    chapter = subjects.values_list(
        'paper_pattern_entry__chapter_topic__subject_chapter__chapter_name', flat=True).distinct()

    for i in range(len(subjects)):
        rm = chapter.filter(
            paper_pattern_entry__chapter_topic__subject_chapter__subject__subject_name=subjects[i],
            paper_pattern_entry__rau_type='R')
        r = rm.aggregate(Avg('marks_obtained'))
        am = chapter.filter(
            paper_pattern_entry__chapter_topic__subject_chapter__subject__subject_name=subjects[i],
            paper_pattern_entry__rau_type='R')
        aa = am.aggregate(Avg('marks_obtained'))
        um = chapter.filter(
            paper_pattern_entry__chapter_topic__subject_chapter__subject__subject_name=subjects[i],
            paper_pattern_entry__rau_type='R')
        u = um.aggregate(Avg('marks_obtained'))


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
        # 'paper_pattern_entry__chapter_topic__subject_chapter__subject__subject_name',
        # \ 'paper_pattern_entry__paper_entry__paper_type__paper_type',
        # 'paper_pattern_entry__paper_question__paper_question_text')

        #############################   MID Performance Graph    ######################################

        # subjects = a.values_list(
        # 'paper_pattern_entry__chapter_topic__subject_chapter__subject__subject_name',
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
            'paper_pattern_entry__chapter_topic__subject_chapter__subject__subject_name',
            flat=True).distinct()

        # for i in range(len(subjects)):
        # ...     print(subjects[i])

        for i in range(len(subjects)):
            r = subjects.filter(paper_pattern_entry__rau_type='R')
            rm = list(r.values_list('marks_obtained', flat=True))
            rk = sum(rm)
            a = subjects.filter(paper_pattern_entry__rau_type='A')
            am = list(a.values_list('marks_obtained', flat=True))
            ak = sum(am)
            u = subjects.filter(paper_pattern_entry__rau_type='U')
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
            'paper_pattern_entry__chapter_topic__subject_chapter__subject__subject_name',
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

        total_mid = ab.aggregate(Sum('paper_pattern_entry__total_marks'))

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
            r = subjects.filter(paper_pattern_entry__rau_type='R')
            rm = list(r.values_list('marks_obtained', flat=True))
            rk = sum(rm)
            a = subjects.filter(paper_pattern_entry__rau_type='A')
            am = list(a.values_list('marks_obtained', flat=True))
            ak = sum(am)
            u = subjects.filter(paper_pattern_entry__rau_type='U')
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
            'paper_pattern_entry__chapter_topic__subject_chapter__subject__subject_name',
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

        total_mid = ab.aggregate(Sum('paper_pattern_entry__total_marks'))

        obtained_mid = ab.aggregate(Sum('marks_obtained'))

        ######################################################################################################################

        # cursor = connection.cursor()
        # cursor.execute(
        #     ''' SELECT sum(marks_obtained), sum(total_marks) FROM map_myschool_user_paper_pattern_entry as m, paper_pattern_entry as a,myschool_user as b, paper_question as c, paper_entry as d, paper_type as t where m.paper_pattern_entry_id=a.paper_pattern_entry_id AND m.myschool_user_id=13 and paper_type = "mid_exam" ''')
        # mid_total_marks = cursor.fetchall()

    else:
        return HttpResponse("<h1>Educator |!| Principal</h1>")


# endregion


# region Bhavesh

def class_detail(request):
    data = sp.MapMySchoolUserStandardSection.objects.all()
    return render(request, 'class_detail.html', {"da": data})


def edit_class(request, standard_section_id):
    std = [1]
    sec = ['A']
    standard_sec = sp.MapMySchoolUserStandardSection.objects.get(pk=standard_section_id)
    return render(request, 'edit_class.html', {'st_se': standard_sec, 'st': std, 'se': sec})


def add_class(request):
    if request.method == 'POST':
        std = request.POST["Standard"]
        sec = request.POST["Section"]
        data = sp.MapMySchoolUserStandardSection(section=sec, standard_id=std)
        data.save()
        return render(request, 'add_class.html')
    else:
        return render(request, 'add_class.html')


def delete_class(request, standard_section_id):
    if request.method == "POST":
        pi = sp.MapMySchoolUserStandardSection.objects.get(standard_section_id=standard_section_id)
        pi.delete()
        return HttpResponseRedirect('/class_detail.html')

# endregion
