from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'login.html')

def add_user(request):
    return render(request, 'auth/user_create.html')

def user_detail(request):
        return render(request, 'auth/user_list.html')

def edit_user(request):
    return render(request, 'edit_user.html')

def add_class(request):
    return render(request, 'add_class.html')

def class_detail(request):
        return render(request, 'class_detail.html')

def edit_class(request):
    return render(request, 'edit_class.html')

def subject_detail(request):
    return render(request, 'subject_detail.html')

def add_subject(request):
    return render(request, 'add_subject.html')

def edit_subject(request):
    return render(request, 'edit_subject.html')

def chapter_detail(request):
    return render(request, 'chapter_detail.html')

def add_chapter(request):
    return render(request, 'add_chapter.html')

def edit_chapter(request):
    return render(request, 'edit_chapter.html')

def topic_detail(request):
    return render(request, 'topic_detail.html')

def add_topic(request):
    return render(request, 'add_topic.html')

def edit_topic(request):
    return render(request, 'edit_topic.html')

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
    return render(request, 'prediction_data.html')