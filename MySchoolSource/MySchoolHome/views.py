import itertools

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Avg
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from MySchool.settings import IS_DEVELOPMENT
from MySchoolHome import models as msh
from StudentPerformance import models as sp
from aagam_packages.django.view_extensions import generic
from aagam_packages.logger.log import log
from aagam_packages.terminal_yoda.terminal_yoda import *
from aagam_packages.utils import utils


# region Aagam Sheth


# region Aagam ModelObjectViews
class MshModelListView(generic.ModelObjectListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = [field for field in self.get_modelobject_fields_label()]
        context['display_fields'] = [field.replace('_', ' ').title() for field in self.get_modelobject_fields_label()]
        context['navbar'] = student_navbar(self.request) if self.request.user.groups.filter(name='Learner').exists() \
            else educator_navbar(self.request) if self.request.user.groups.filter(name='Educator').exists() \
            else principal_navbar() if self.request.user.groups.filter(name='Principal').exists() \
            else PermissionError
        return context


class MshModelUpdateView(generic.ModelObjectUpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = student_navbar(self.request) if self.request.user.groups.filter(name='Learner').exists() \
            else educator_navbar(self.request) if self.request.user.groups.filter(name='Educator').exists() \
            else principal_navbar() if self.request.user.groups.filter(name='Principal').exists() \
            else PermissionError
        return context


# endregion


@login_required()
def home(request):
    yoda_saberize_print(request.get_full_path(), YodaSaberColor.BLACK, YodaSaberColor.LIGHTGOLDENRODYELLOW)

    if Group.objects.get(name='Learner') in request.user.groups.all():
        return redirect("MySchoolHome:student_dashboard")
    elif Group.objects.get(name='Educator') in request.user.groups.all():
        return redirect("MySchoolHome:educator_dashboard")
    elif Group.objects.get(name='Principal') in request.user.groups.all():
        return redirect("MySchoolHome:principal_dashboard")
    elif Group.objects.get(name='Staff') in request.user.groups.all():
        return redirect("admin/")
    else:
        return HttpResponse(status=403)


# region Role Navbars
def student_navbar(request):
    map_id = sp.MapMySchoolUserStandardSection.objects. \
        select_related('myschool_user__auth_user') \
        .filter(myschool_user__auth_user=request.user)
    map_id = map_id.values('pk', 'section', 'standard', 'myschool_user__pk',
                           'myschool_user__auth_user__username', 'status')
    map_active_id = map_id.filter(status=True)
    sections = map_id.values('section').distinct()
    subject = sp.TblSubject.objects.filter(standard__in=map_active_id.values("standard"))
    context = {'standard_section': map_id.filter(status=True),
               'section': sections,
               'standard_section_current': map_active_id.first(),
               'subject': subject}
    return context


def educator_navbar(request):
    map_id = sp.MapMySchoolUserSubject.objects.filter(
        myschool_user=msh.MySchoolUser.objects.get(auth_user=request.user))
    standard = map_id.values('subject__standard').distinct()
    sections = sp.MapMySchoolUserStandardSection.objects.values('section').distinct()
    context = {'user_subject': map_id,
               'section': sections,
               'standard': standard}
    return context


def principal_navbar():
    standard = sp.TblStandard.objects.all()
    sections = sp.MapMySchoolUserStandardSection.objects.values('section').distinct()
    context = {'section': sections,
               'standard': standard}
    return context


# endregion


# region Role Dashboards
@login_required()
def student_dashboard(request):
    log.debug("Student Dashboard")
    graph_data = get_student_dashboard_graph(request)
    context = {'page_context': {'title': "MySchool Student Dashboard", 'titleTag': 'MySchool'},
               'navbar': student_navbar(request),
               'graph_data': graph_data
               }
    yoda_saberize_print(request.get_full_path().__contains__('/student/'), YodaSaberColor.BLACK,
                        YodaSaberColor.LIGHTGOLDENRODYELLOW)
    return render(request, 'dashboard/student_dashboard.html', context)


@login_required()
def educator_dashboard(request):
    graph_data = get_educator_dashboard()
    context = {'page_context': {'title': "MySchool Educator Dashboard",
                                'titleTag': 'MySchool'},
               'navbar': educator_navbar(request),
               'graph_data': graph_data}
    return render(request, 'dashboard/educator_dashboard.html', context)


@login_required()
def principal_dashboard(request):
    navbar = principal_navbar()

    subject_educator = sp.MapMySchoolUserSubject.objects.filter(
        subject__standard=request.GET.get('standard', navbar['standard'].first().standard))

    map_id = sp.MapMySchoolUserStandardSection.objects \
        .filter(standard=request.GET.get('standard', navbar['standard'].first().standard),
                section=request.GET.get('section', navbar['section'].first()['section']), status=True)

    subject = sp.TblSubject.objects.filter(standard=request.GET.get('standard', navbar['standard'].first().standard))

    rau = {'r': 0, 'a': 0, 'u': 0}

    if (not IS_DEVELOPMENT) or (request.GET.get('standard', navbar['standard'].first().standard) in ['9', '10']):
        rau = get_principal_dashboard_rau_count_graph(request, subject, map_id)
        yoda_saberize_print(rau)

    context = {'page_context': {'title': "MySchool Principal Dashboard",
                                'titleTag': 'MySchool'},
               'subject_educators': subject_educator,
               'learners': map_id,
               'navbar': navbar,
               'rau': rau}
    return render(request, 'dashboard/principal_dashboard.html', context)


# endregion


# region Dashboard Graph Functions
def get_principal_dashboard_rau_count_graph(request, subject, learner):
    total_marks_obtained = sp.MapStudentPaperPatternEntry.objects.filter(
        map_myschool_user_standard_section__in=learner,
        paper_pattern_entry__paper_entry__subject__in=subject,
    ).values('paper_pattern_entry__rau_type').annotate(total_marks_obtained=Avg('marks_obtained'),
                                                       outoff_total_marks=Avg('paper_pattern_entry__total_marks'))

    yoda_saberize_print(total_marks_obtained, YodaSaberColor.RED, YodaSaberColor.CORNFLOWERBLUE)

    r = total_marks_obtained.filter(paper_pattern_entry__rau_type='R')
    a = total_marks_obtained.filter(paper_pattern_entry__rau_type='A')
    u = total_marks_obtained.filter(paper_pattern_entry__rau_type='U')

    r = (int(((dict(r[0])['total_marks_obtained']) /
              (dict(r[0])['outoff_total_marks'])) * 100))
    a = (int(((dict(a[0])['total_marks_obtained']) /
              (dict(a[0])['outoff_total_marks'])) * 100))
    u = (int(((dict(u[0])['total_marks_obtained']) /
              (dict(u[0])['outoff_total_marks'])) * 100))

    context = {
        'r': r,
        'a': a,
        'u': u
    }

    return context


# endregion


# region Development Info
def sitemap(request):
    python_lines = str(utils.count_lines("*.py"))
    html_lines = str(utils.count_lines("*.html"))
    text_lines = str(utils.count_lines("*.txt"))
    json_lines = str(utils.count_lines("*.json"))
    pickled_lines = str(utils.count_lines("*.pickle"))
    total_lines = str(utils.count_lines("*.*"))
    html_static_files_lines = str(utils.count_lines("*.*", "aagam_static"))
    context = f'''
    <html>
        <head>
            <title>Aagam Sheth Site Stats</title>
        </head>
        <body>
            <h1>Python Lines : {python_lines} </h1>
            <h1>HTML Lines : {html_lines} </h1>
            <h1>Text Lines : {text_lines} </h1>
            <h1>Json Lines : {json_lines} </h1>
            <h1>Pickled Lines : {pickled_lines} </h1>
            <h1>Total Lines : {int(total_lines) - int(html_static_files_lines) - int(pickled_lines)} </h1>
            <h1>Total Lines including static files : {total_lines} </h1>
        </body>
    </html>
    '''
    return HttpResponse(context)


# endregion


# endregion


# region Yash
def get_student_dashboard_graph(request):
    navbar_context = student_navbar(request)
    standard = request.GET.get('standard', navbar_context['standard_section_current']['standard'])

    current_my_school_user = \
        sp.MapMySchoolUserStandardSection.objects.get(myschool_user__auth_user=request.user,
                                                      standard=standard,
                                                      status=True)
    yoda_saberize_print(current_my_school_user, YodaSaberColor.HOTPINK)

    stud = sp.MapStudentPaperPatternEntry.objects.all().filter(
        map_myschool_user_standard_section=current_my_school_user).select_related('paper_pattern_entry')

    r_s = stud.filter(paper_pattern_entry__rau_type='R').aggregate(Avg('marks_obtained'))
    a_s = stud.filter(paper_pattern_entry__rau_type='A').aggregate(Avg('marks_obtained'))
    u_s = stud.filter(paper_pattern_entry__rau_type='U').aggregate(Avg('marks_obtained'))

    subjects = stud.values_list(
        'paper_pattern_entry__chapter_topic__subject_chapter__subject__subject_name',
        flat=True).distinct()

    marks = ""
    for i in range(len(subjects)):
        marks = (subjects.filter(
            paper_pattern_entry__chapter_topic__subject_chapter__subject__subject_name=subjects[i])) \
            .aggregate(Avg('marks_obtained'))

    assignments = stud.filter(
        paper_pattern_entry__paper_entry__paper_type__paper_type='Assignment').aggregate(Avg('marks_obtained'))
    pra = stud.filter(
        paper_pattern_entry__paper_entry__paper_type__paper_type='Practical').aggregate(Avg('marks_obtained'))
    uni = stud.filter(
        paper_pattern_entry__paper_entry__paper_type__paper_type='Unit').aggregate(Avg('marks_obtained'))
    mid = stud.filter(
        paper_pattern_entry__paper_entry__paper_type__paper_type='Mid').aggregate(Avg('marks_obtained'))
    fin = stud.filter(
        paper_pattern_entry__paper_entry__paper_type__paper_type='Final').aggregate(Avg('marks_obtained'))

    context = {
        'skill_graph': {
            'r_s': r_s,
            'a_s': a_s,
            'u_s': u_s
        },
        'subjects': subjects,
        'subject_marks': marks,
        'subject_paper_marks': {
            'assignments': assignments,
            'practicals': pra,
            'unit': uni,
            'mid': mid,
            'final': fin
        }

    }
    return context


# endregion


# region Bhavesh


def get_educator_graph_details():
    data = sp.MapStudentPaperPatternEntry.objects.select_related(
        'map_myschool_user_standard_section__myschool_user__auth_user')
    top_performer = data.filter(marks_obtained__gt=21).values(
        'map_myschool_user_standard_section__myschool_user__auth_user__username')
    potential_performer = data.filter(marks_obtained__gt=15).values(
        'map_myschool_user_standard_section__myschool_user__auth_user__username')
    lower_performer = data.filter(marks_obtained__lte=15).values(
        'map_myschool_user_standard_section__myschool_user__auth_user__username')
    marks = data.values('marks_obtained',
                        'map_myschool_user_standard_section__myschool_user__auth_user__username').order_by(
        'marks_obtained')
    return {'t': top_performer, 'p': potential_performer, 'l': lower_performer, 'marks': marks}


def graph_teacher_dashboard(user_id):
    sub = "Mathematics 9709"
    std = 9
    sec = 'C'
    data = sp.MapStudentPaperPatternEntry.objects.select_related('paper_pattern_entry'). \
        filter(map_myschool_user_standard_section__myschool_user=user_id,
               paper_pattern_entry__paper_entry__paper_type__paper_type__contains="Unit Test")
    marks = data.filter(
        paper_pattern_entry__chapter_topic__subject_chapter__subject__subject_name=sub,
        map_myschool_user_standard_section__standard=std,
        map_myschool_user_standard_section__section=sec,
    )
    am = list(marks.values_list('marks_obtained', flat=True))
    actual_marks = sum(am)
    dic = {
        user_id: actual_marks,
    }
    return dic


def Overall_class_performance(paperType):
    sub = "Mathematics 9709"
    std = 9
    sec = 'C'
    data = sp.MapStudentPaperPatternEntry.objects.select_related('paper_pattern_entry'). \
        filter(paper_pattern_entry__paper_entry__paper_type__paper_type__contains=paperType)
    marks = data.filter(
        paper_pattern_entry__chapter_topic__subject_chapter__subject__subject_name=sub,
        map_myschool_user_standard_section__standard=std,
        map_myschool_user_standard_section__section=sec,
    )
    actual_marks = marks.aggregate(Avg('marks_obtained'))
    return actual_marks


def get_educator_dashboard():
    std = 9
    sec = 'C'
    data = sp.MapStudentPaperPatternEntry.objects.select_related(
        'map_myschool_user_standard_section__myschool_user__auth_user')
    tp = data.filter(marks_obtained__gt=21).values(
        'map_myschool_user_standard_section__myschool_user__auth_user__username')
    pp = data.filter(marks_obtained__gt=15).values(
        'map_myschool_user_standard_section__myschool_user__auth_user__username')
    lp = data.filter(marks_obtained__lte=15).values(
        'map_myschool_user_standard_section__myschool_user__auth_user__username')
    userId = list(
        sp.MapStudentPaperPatternEntry.objects.values_list('map_myschool_user_standard_section__myschool_user',
                                                           flat=True).
            distinct())
    minMarks = {}
    for i in userId:
        minMarks.update(graph_teacher_dashboard(i))
    minMarks_values = sorted(minMarks.values())  # Sort the values
    sorted_minMarks = {}

    for i in minMarks_values:
        for k in minMarks.keys():
            if minMarks[k] == i:
                sorted_minMarks[k] = minMarks[k]
                break
    sorted_Keys = (list(sorted_minMarks.keys()))
    uname = sp.MySchoolUser.objects.select_related('auth_user').values('auth_user__username')
    actual_user = []
    for i in sorted_Keys:
        actual_user.append(list(uname.values_list('auth_user__username', flat=True).filter(myschool_user_id=i)))
    sorted_user = list(itertools.chain.from_iterable(actual_user))[:10]
    sorted_values = (list(sorted_minMarks.values()))[:10]
    unit_Marks = Overall_class_performance("Unit Test")
    mid_sem = Overall_class_performance("Mid Unit Test")
    assignments = Overall_class_performance("Assignment")
    context = {
        't': tp, 'p': pp, 'l': lp,
        'user': sorted_user,
        'values': sorted_values,
        'Unit_Marks': unit_Marks,
        'Mid_Marks': mid_sem,
        'Assignment': assignments,
    }
    return context

# endregion
