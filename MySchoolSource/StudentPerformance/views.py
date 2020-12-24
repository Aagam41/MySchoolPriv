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

from MySchoolHome import views as mshv

from StudentPerformancePrediction.MachineLearningModels import KNNmdl
from StudentPerformancePrediction.MachineLearningModels import LinearRegression

from aagam_packages.django.view_extensions import generic
from aagam_packages.utils import utils
from aagam_packages.terminal_yoda.terminal_yoda import *
from aagam_packages.terminal_yoda import terminal_utils


# Create your views here.


def performance_panel(request, **kwargs):
    if request.user.groups.filter(name='Learner').exists():
        return HttpResponse("<h1>Student</h1>")
    elif request.user.groups.filter(name='Educator').exists():
        educator_context = mshv.educator_navbar(request)
        standard = request.GET.get('standard', educator_context['standard'].first()['subject__standard'])
        section = request.GET.get('section', educator_context['section'].first()['section'])
        learner = sp.MapMySchoolUserStandardSection.objects\
            .filter(standard_section__standard=standard, standard_section__section=section, status=True)\
            .values_list("myschool_user__pk")
        learner_detail = msh.MySchoolUser.objects.filter(myschool_user_id__in=learner)
        context = {
            'learners': learner_detail,
            'performance_type': kwargs.get('performance_type'),
            'navbar': educator_context,
        }
        return render(request, 'StudentPerformance/educator_panel_student_list.html', context)
