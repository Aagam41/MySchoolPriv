import json
import random

from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.models import User, Group

from MySchoolHome import models as msh
from StudentPerformance import models as sp

from aagam_packages.terminal_yoda.terminal_yoda import *

# Create your views here.


def test(request):
    # # Auth.User
    # with open('D:\\Aagam Projects\\Python\\Django\\MySchool\\MySchoolSource\\JsonData\\Latest\\user.json') as f:
    #     user = json.load(f)
    # for p in user:
    #     p = User(username=p['username'], password=p['password'], first_name=p['first_name'], last_name=p['last_name'],
    #              email=p['email'])
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
    # # TblSubject
    # with open('D:\\Aagam Projects\\Python\\Django\\MySchool\\MySchoolSource\\JsonData\\Latest\\subject.json') as f:
    #     user = json.load(f)
    # for p in user:
    #     p = sp.TblSubject(subject_name=p['subject_name'], standard=sp.Standard.objects.get(standard=p['standard']),
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

    # # StandardSection
    # for i in range(1, 13):  # for 1 to 12, default starts for 0 and ends before stop value
    #     for j in ['A', 'B', 'C']:
    #         p = sp.StandardSection(standard=sp.Standard.objects.get(standard=i), section=j)
    #         p.save()

    # # MySchoolUser
    # with open(
    #        'D:\\Aagam Projects\\Python\\Django\\MySchool\\MySchoolSource\\JsonData\\Latest\\user.json') as f:
    #     user = json.load(f)
    # for p in user:
    #     p = msh.MySchoolUser(auth_user=User.objects.get(username=p['username']))
    #     p.save()

    # MapMySchoolUserStandardSection
    # auth_user1 = User.objects.filter(groups=1)
    # for auth in auth_user1:
    #     stud = msh.MySchoolUser.objects.filter(auth_user=auth)
    #     print(stud)
    #     stan = random.randint(1, 12)
    #     print(str(stan))
    #     sec = random.choice(sp.StandardSection.objects.filter(standard=stan))
    #     print(sec)
    #     stss = sp.MapMySchoolUserStandardSection(myschool_user=stud[0],
    #                                              standard_section=sec)
    #     stss.save()
    #

    return HttpResponse('<h1>Done</h1>')
