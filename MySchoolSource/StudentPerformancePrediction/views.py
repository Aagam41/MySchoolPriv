from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from MySchoolHome import views

# Create your views here.

def student_prediction(request):
    context = {'page_context': {'title': "MySchool Student Dashboard", 'titleTag': 'MySchool'},
               'search_name': '',
               'navbar': views.student_navbar(request)}
    return render(request, 'StudentPerformancePrediction/student_prediction.html', context)
