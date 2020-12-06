from django.shortcuts import render
from MySchoolQuery.query import student
# Create your views here.
def test():
    htmtxtmyschooluser = "aagam"
    myschool_user = student(htmtxtmyschooluser)