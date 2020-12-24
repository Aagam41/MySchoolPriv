import json
import random

from django.apps import apps
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from MySchoolHome import forms
from django.core import serializers

from MySchoolHome import models as msh
from StudentPerformance import models as sp
from StudentPerformancePrediction import models as spp

from StudentPerformancePrediction.MachineLearningModels import KNNmdl
from StudentPerformancePrediction.MachineLearningModels import LinearRegression

from aagam_packages.django.view_extensions import generic
from aagam_packages.utils import utils
from aagam_packages.terminal_yoda.terminal_yoda import *
from aagam_packages.terminal_yoda import terminal_utils

# Create your views here.


class MshModelListView(generic.ModelObjectListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = [field for field in self.get_modelobject_fields_label()]
        context['display_fields'] = [field.replace('_', ' ').title() for field in self.get_modelobject_fields_label()]
        context['navbar'] = student_navbar(self.request) if self.request.user.groups.filter(name='Learner').exists() \
            else educator_navbar(self.request) if self.request.user.groups.filter(name='Educator').exists() \
            else principal_navbar(self.request) if self.request.user.groups.filter(name='Principal').exists() \
            else PermissionError
        return context


class MshModelUpdateView(generic.ModelObjectUpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = student_navbar(self.request) if self.request.user.groups.filter(name='Learner').exists() \
            else educator_navbar(self.request) if self.request.user.groups.filter(name='Educator').exists() \
            else principal_navbar(self.request) if self.request.user.groups.filter(name='Principal').exists() \
            else PermissionError
        return context


@login_required()
def home(request):
    if Group.objects.get(name='Learner') in request.user.groups.all():
        return redirect("MySchoolHome:student_dashboard")
    elif Group.objects.get(name='Educator') in request.user.groups.all():
        return redirect("MySchoolHome:educator_dashboard")
    elif Group.objects.get(name='Principal') in request.user.groups.all():
        return HttpResponse("MySchoolHome:principal_dashboard")
    else:
        return HttpResponse(status=403)


def student_navbar(request):
    map_id = sp.MapMySchoolUserStandardSection.objects.\
        select_related('standard_section','myschool_user__auth_user')\
        .filter(myschool_user__auth_user=request.user)
    map_id = map_id.values('pk', 'standard_section__section', 'standard_section__standard', 'myschool_user__pk',
                           'myschool_user__auth_user__username', 'status')
    map_active_id = map_id.get(status=True)
    sections = sp.StandardSection.objects.all().values('section').distinct()
    subject = sp.TblSubject.objects.filter(standard__lte=map_active_id['standard_section__standard'])
    context = {'standard_section': map_id,
               'section': sections,
               'standard_section_current': map_active_id,
               'subject': subject}
    return context


def educator_navbar(request):
    map_id = sp.MapMySchoolUserSubject.objects.filter(myschool_user=msh.MySchoolUser.objects.get(auth_user=request.user))
    standard = map_id.values('subject__standard').distinct()
    sections = sp.StandardSection.objects.all().values('section').distinct()
    context = {'user_subject': map_id,
               'section': sections,
               'standard': standard}
    return context


def principal_navbar(request):
    map_id = sp.MapMySchoolUserSubject.objects.select_related('subject__subject_name')\
        .filter(myschool_user=msh.MySchoolUser.objects.get(auth_user=request.user))
    standard = map_id.values('standard').distinct()
    sections = sp.StandardSection.objects.all().values('section').distinct()
    context = {'standard_section': map_id,
               'section': sections,
               'standard': standard}
    return context


@login_required()
def student_dashboard(request):
    context = {'page_context': {'title': "MySchool Student Dashboard", 'titleTag': 'MySchool'},
               'navbar': student_navbar(request)}
    return render(request, 'dashboard/student_dashboard.html', context)


@login_required()
def educator_dashboard(request):
    context = {'page_context': {'title': "MySchool Educator Dashboard",
                                'titleTag': 'MySchool'},
               'navbar': educator_navbar(request)}
    return render(request, 'dashboard/educator_dashboard.html', context)


@login_required()
def principal_dashboard(request):
    context = {'page_context': {'title': "MySchool Principal Dashboard",
                                'titleTag': 'MySchool'}}
    return render(request, 'dashboard/principal_dashboard.html', context)


def sitemap(request):
    python_lines = str(utils.count_lines("*.py"))
    html_lines = str(utils.count_lines("*.html"))
    text_lines = str(utils.count_lines("*.txt"))
    json_lines = str(utils.count_lines("*.json"))
    context = {'py': python_lines, 'html': html_lines, 'txt': text_lines, 'json': json_lines}
    return render(request, "MySchool_site_nav.html", context)


def load_database(request):
    # # Auth.User
    # p = User.objects.create_superuser(username='Aagam41', password='MySchool@123', first_name='Aagam',
    #                                   last_name='Sheth', email='aagam.h.sheth@icloud.com')
    # p.save()
    # p = User.objects.create_superuser(username='Bhavesh03', password='MySchool@123', first_name='Bhavesh',
    #                                   last_name='Bhavnani', email='test@gmail.com')
    # p.save()
    # p = User.objects.create_superuser(username='Nishil53', password='MySchool@123', first_name='Aagam',
    #                                   last_name='Shah', email='test1@gmail.com')
    # p.save()
    # p = User.objects.create_superuser(username='Brijesh05', password='MySchool@123', first_name='Aagam',
    #                                   last_name='Sukhadiya', email='test2@gmail.com')
    # p.save()
    # p = User.objects.create_superuser(username='Yash01', password='MySchool@123', first_name='Yash',
    #                                   last_name='Akbari', email='test3@gmail.com')
    # p.save()
    #
    # # Auth.Group
    # g1 = Group.objects.create(name='Learner')
    # g1.save()
    # g1 = Group.objects.create(name='Educator')
    # g1.save()
    #
    #
    # Auth.User
    # with open('D:\\Aagam Projects\\Python\\Django\\MySchool\\MySchoolSource\\JsonData\\Latest\\user.json') as f:
    #     user = json.load(f)
    # for p in user:
    #     p = User(username=p['username'], password=p['password'], first_name=p['first_name'], last_name=p['last_name'],
    #              email=p['email'])
    #     p.save()
    #     group1 = Group.objects.get(id=1)
    #     group1.user_set.add(p)
    #
    # with open('D:\\Aagam Projects\\Python\\Django\\MySchool\\MySchoolSource\\JsonData\\Latest\\user.json') as f:
    #     user = json.load(f)
    # for p in user:
    #     p = User(username=p['username']+'12we3', password=p['password'], first_name=p['first_name'], last_name=p['last_name'],
    #              email='12we3' + p['email'])
    #     p.save()
    #     group1 = Group.objects.get(id=1)
    #     group1.user_set.add(p)
    #
    # with open('D:\\Aagam Projects\\Python\\Django\\MySchool\\MySchoolSource\\JsonData\\Latest\\user.json') as f:
    #     user = json.load(f)
    # for p in user:
    #     p = User(username=p['username']+'12w113', password=p['password'], first_name=p['first_name'], last_name=p['last_name'],
    #              email='12we3'+p['email'])
    #     p.save()
    #     group1 = Group.objects.get(id=1)
    #     group1.user_set.add(p)
    #
    # with open('D:\\Aagam Projects\\Python\\Django\\MySchool\\MySchoolSource\\JsonData\\Latest\\user.json') as f:
    #     user = json.load(f)
    # for p in user:
    #     p = User(username=p['username']+'12weasc', password=p['password'], first_name=p['first_name'], last_name=p['last_name'],
    #              email='12we3'+p['email'])
    #     p.save()
    #     group1 = Group.objects.get(id=1)
    #     group1.user_set.add(p)
    #
    # with open('D:\\Aagam Projects\\Python\\Django\\MySchool\\MySchoolSource\\JsonData\\Latest\\user.json') as f:
    #     user = json.load(f)
    # for p in user:
    #     p = User(username=p['username']+'12wqwe3', password=p['password'], first_name=p['first_name'], last_name=p['last_name'],
    #              email='12wesds3' + p['email'])
    #     p.save()
    #     group1 = Group.objects.get(id=1)
    #     group1.user_set.add(p)
    #
    # with open('D:\\Aagam Projects\\Python\\Django\\MySchool\\MySchoolSource\\JsonData\\Latest\\user.json') as f:
    #     user = json.load(f)
    # for p in user:
    #     p = User(username=p['username']+'sbf12w113', password=p['password'], first_name=p['first_name'], last_name=p['last_name'],
    #              email='12swe3'+p['email'])
    #     p.save()
    #     group1 = Group.objects.get(id=1)
    #     group1.user_set.add(p)
    #
    # with open('D:\\Aagam Projects\\Python\\Django\\MySchool\\MySchoolSource\\JsonData\\Latest\\user.json') as f:
    #     user = json.load(f)
    # for p in user:
    #     p = User(username=p['username']+'b12weasc', password=p['password'], first_name=p['first_name'], last_name=p['last_name'],
    #              email='1ert2htwe3'+p['email'])
    #     p.save()
    #     group1 = Group.objects.get(id=1)
    #     group1.user_set.add(p)
    #
    #     # Auth.User for teacher
    # with open('D:\\Aagam Projects\\Python\\Django\\MySchool\\MySchoolSource\\JsonData\\Latest\\teacher.json') as f:
    #     user = json.load(f)
    # for p in user:
    #     p = User(username=p['username'], password=p['password'], first_name=p['first_name'],
    #              last_name=p['last_name'],
    #              email=p['email'])
    #     p.save()
    #     group1 = Group.objects.get(id=2)
    #     group1.user_set.add(p)
    #
    # # Standard
    # for i in range(1,13):
    #     s = sp.TblStandard.objects.create(standard=i)
    #     s.save()
    #
    # # TblSubject
    # with open('D:\\Aagam Projects\\Python\\Django\\MySchool\\MySchoolSource\\JsonData\\Latest\\subject.json') as f:
    #     user = json.load(f)
    # for p in user:
    #     p = sp.TblSubject(subject_name=p['subject_name'], standard=sp.TblStandard.objects.get(standard=p['standard']),
    #                       remembrance_credit=p['remembrance_credit'],
    #                       applied_knowledge_credit=p['applied_knowledge_credit'],
    #                       understanding_credit=p['understanding_credit'], subject_credit=p['subject_credit'])
    #     p.save()
    #
    #
    # # SubjectChapter
    # with open('D:\\Aagam Projects\\Python\\Django\\MySchool\\MySchoolSource\\JsonData\\Latest\\subjectchapter.json') as f:
    #     user = json.load(f)
    # for p in user:
    #     p = sp.SubjectChapter(subject=sp.TblSubject.objects.get(subject_name=p['subject']),
    #                           chapter_id=p['chapter_id'], chapter_name=p['chapter_name'],
    #                           remembrance_credit=p['remembrance_credit'],
    #                           applied_knowledge_credit=p['applied_knowledge_credit'],
    #                           understanding_credit=p['understanding_credit'], chapter_credit=p['chapter_credit'])
    #     p.save()
    #
    # # ChapterTopic
    # with open(
    #         'D:\\Aagam Projects\\Python\\Django\\MySchool\\MySchoolSource\\JsonData\\Latest\\chaptertopic2.json') as f:
    #     user = json.load(f)
    # for p in user:
    #     subject1 = sp.TblSubject.objects.get(subject_name=p['subject'])
    #     chapter1 = sp.SubjectChapter.objects.filter(subject=subject1).get(chapter_id=p['chapter'])
    #     p = sp.ChapterTopic(subject_chapter=chapter1,
    #                         topic_id=p['topic_id'], topic_name=p['topic_name'])
    #     p.save()
    #
    # # MySchoolUser  Educator
    # with open(
    #        'D:\\Aagam Projects\\Python\\Django\\MySchool\\MySchoolSource\\JsonData\\Latest\\teacher.json') as f:
    #     user = json.load(f)
    # for p in user:
    #     p = msh.MySchoolUser(auth_user=User.objects.get(username=p['username']))
    #     p.save()
    #
    # # StandardSection
    # for i in range(1, 13):  # for 1 to 12, default starts for 0 and ends before stop value
    #     for j in ['A', 'B']:
    #         p = sp.StandardSection(standard=sp.TblStandard.objects.get(standard=i), section=j)
    #         p.save()
    #     rand = random.randint(0, 1)
    #     if 1 == rand:
    #         p = sp.StandardSection(standard=sp.TblStandard.objects.get(standard=i), section="C")
    #         p.save()
    #         p = sp.StandardSection(standard=sp.TblStandard.objects.get(standard=i), section="D")
    #         p.save()
    #     else:
    #         p = sp.StandardSection(standard=sp.TblStandard.objects.get(standard=i), section="C")
    #         p.save()
    #
    #
    # # MySchoolUser
    # user = User.objects.all()
    #
    # for p in user:
    #     p = msh.MySchoolUser(auth_user=p)
    #     p.save()
    #
    # # MapMySchoolUserStandardSection
    # auth_user1 = User.objects.filter(groups=1)
    # for auth in auth_user1:
    #     stud = msh.MySchoolUser.objects.filter(auth_user=auth)
    #     stan = random.randint(1, 12)
    #     sec = random.choice(sp.StandardSection.objects.filter(standard=stan))
    #     stss = sp.MapMySchoolUserStandardSection(myschool_user=stud[0],
    #                                              standard_section=sec, status=True)
    #     stss.save()

    # Serialize tables
    # a = sp.PaperQuestion.objects.all()
    # serialized = serializers.serialize('json', a)
    # yoda_saberize_print(serialized, YodaSaberColor.BLACK, YodaSaberColor.CORNFLOWERBLUE)

    return HttpResponse("<h1>Done</h1>")
