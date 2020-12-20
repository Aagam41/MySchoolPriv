from django.shortcuts import render
from StudentPerformance import models as ap
from aagam_packages.terminal_yoda.terminal_yoda import *
# Create your views here.

def login(request):
    return render(request, 'registration/login.html')

def add_user(request):
    return render(request, 'index.html')

def user_detail(request):
        return render(request, 'auth/user_list.html')

def edit_user(request):
    return render(request, 'notNeeded/user_update.html')

def add_class(request):
    return render(request, 'StudentPerformance/../zzzbrijtemplates/standard_create.html')

def class_detail(request):
    yoda_saberize_print("Aagam", YodaSaberColor.WHITE, YodaSaberColor.HOTPINK)
    data = ap.StandardSection.objects.values('standard', 'section')
    return render(request, 'StudentPerformance/../zzzbrijtemplates/standardsection_list.html', {'da': data})

def edit_class(request):
    return render(request, 'notNeeded/standard_update.html')

def subject_detail(request):
    return render(request, 'StudentPerformance/../zzzbrijtemplates/tblsubject_list.html')

def add_subject(request):
    return render(request, 'StudentPerformance/../zzzbrijtemplates/tblsubject_create.html')

def edit_subject(request):
    return render(request, 'notNeeded/tblsubject_update.html')

def chapter_detail(request):
    return render(request, 'StudentPerformance/../zzzbrijtemplates/subjectchapter_list.html')

def add_chapter(request):
    return render(request, 'StudentPerformance/../zzzbrijtemplates/subjectchapter_create.html')

def edit_chapter(request):
    return render(request, 'StudentPerformance/../zzzbrijtemplates/subjectchapter_update.html')

def topic_detail(request):
    return render(request, 'StudentPerformance/../zzzbrijtemplates/chaptertopic_list.html')

def add_topic(request):
    return render(request, 'StudentPerformance/../zzzbrijtemplates/chaptertopic_create.html')

def edit_topic(request):
    return render(request, 'notNeeded/chaptertopic_update.html')

def teac_dashboard(request):
    return render(request, 'Educator/teac_dashboard.html')

def teac_prediction(request):
    return render(request, 'Educator/teac_prediction.html')

def teac_feedback(request):
    return render(request, 'Educator/teac_feedback.html')

def stu_prediction(request):
    return render(request, 'student_prediction.html')

def stu_dashboard(request):
    return render(request, 'stu_dashboard.html')

def stu_feedback(request):
    return render(request, 'stu_feedback.html')

def prin_dashboard(request):
    return render(request, 'Educator/prin_dashboard.html')

def prin_feedback(request):
    return render(request, 'Educator/prin_feedback.html')

def prin_prediction(request):
    return render(request, 'Educator/prin_prediction.html')

def prediction_data(request):
    return render(request, 'StudentPerformancePrediction/studentefficacy_create.html')