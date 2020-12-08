from django.shortcuts import render
from django.http.response import HttpResponse
from django.template import Template

from MySchoolQuery import query
from StudentPerformance import models as sp

from django.contrib.auth.models import User


# Create your views here.


def test(request):
    logintxt = "aagam"
    a = query.get_myschool_user(logintxt)
    query.marks(a, "jdjfhgf")
    print("id: " + str(a))
    return HttpResponse(a)
