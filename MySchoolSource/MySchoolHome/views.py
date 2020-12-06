from django.shortcuts import render
from django.http.response import HttpResponse
from django.template import Template

from MySchoolQuery import query

from django.contrib.auth.models import User


# Create your views here.


def test(request):
    a = query.get_myschool_user("AagamSheth")
    return HttpResponse(a)
