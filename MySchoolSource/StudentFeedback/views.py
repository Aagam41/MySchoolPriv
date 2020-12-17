from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'login.html')

def add_user(request):
    return render(request, 'auth/user_create.html')

def user_detail(request):
        return render(request, 'auth/user_list.html')

def edit_user(request):
    return render(request, 'user_update.html')

def add_class(request):
    return render(request, 'standard_create.html')

def class_detail(request):
        return render(request, 'standardsection_list.html')

def edit_class(request):
    return render(request, 'standard_update.html')

def subject_detail(request):
    return render(request, 'subject_list.html')

def add_subject(request):
    return render(request, 'tblsubject_create.html')

def edit_subject(request):
    return render(request, 'tblsubject_update.html')

def chapter_detail(request):
    return render(request, 'subjectchapter_list.html')

def add_chapter(request):
    return render(request, 'subjectchapter_create.html')

def edit_chapter(request):
    return render(request, 'subjectchapter_update.html')

def topic_detail(request):
    return render(request, 'chaptertopic_list.html')

def add_topic(request):
    return render(request, 'chaptertopic_create.html')

def edit_topic(request):
    return render(request, 'chaptertopic_update.html')

def teac_dashboard(request):
    return render(request, 'teac_dashboard.html')

def teac_prediction(request):
    return render(request, 'teac_prediction.html')

def teac_feedback(request):
    return render(request, 'teac_feedback.html')

def stu_prediction(request):
    return render(request, 'stu_prediction.html')

def stu_dashboard(request):
    return render(request, 'stu_dashboard.html')

def stu_feedback(request):
    return render(request, 'stu_feedback.html')

def prin_dashboard(request):
    return render(request, 'prin_dashboard.html')

def prin_feedback(request):
    return render(request, 'prin_feedback.html')

def prin_prediction(request):
    return render(request, 'prin_prediction.html')

def prediction_data(request):
    return render(request, 'studentefficacy_create.html')