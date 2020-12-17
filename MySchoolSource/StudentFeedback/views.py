from django.shortcuts import render, HttpResponseRedirect
from MySchoolHome import models as msh
from StudentPerformance import models as sp
from StudentPerformancePrediction import models as spp



def add_user(request):
    return render(request, 'add_user.html')

def user_detail(request):
    return render(request, 'user_detail.html')

def edit_user(request):
    return render(request, 'edit_user.html')

def class_detail(request):
    data = sp.StandardSection.objects.values('standard', 'section')
    return render(request, 'class_detail.html', {'da': data})

'''def edit_class(request, standard):
    if request.method == 'POST':
        pi = sp.StandardSection.objects.get(pk=standard)
        std = request.POST["Standard"]
        sec = request.POST["Section"]
        data = sp.StandardSection(section=sec, standard=std, instance=pi)
        data.save()
    else:
        pi = sp.StandardSection.objects.get(pk=standard)
        data = sp.StandardSection(instance=pi)
        return render(request, 'edit_class.html', {'da': data})'''



def add_class(request):
    if request.method == 'POST':
        std = request.POST["Standard"]
        sec = request.POST["Section"]
        data = sp.StandardSection(section=sec, standard_id=std)
        data.save()
        #return HttpResponseRedirect('/class_detail')
        return render(request, 'add_class.html')
    else:
        return render(request, 'add_class.html')
    return render(request, 'add_class.html')

def delete_class(request,standard):
    if request.method == "POST":
        pi = sp.StandardSection.objects.get(pk=standard)
        pi.delete()
        return HttpResponseRedirect('/class_detail')
        #return render(request, 'class_detail.html')


def get_teacher_dashboard(request):
    return render(request, 'teac_dashboard.html')


def get_student_prediction(request):
    return render(request, 'stu_prediction.html')

def get_teacher_prediction(request):
    return render(request, 'teac_prediction.html')

def get_principal_prediction(request):
    return render(request, 'prin_prediction.html')

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
    return render(request, 'subjectchapter_list.html')

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