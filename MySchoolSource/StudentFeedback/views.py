from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from StudentPerformance import models
from MySchoolHome import views
#from StudentFeedback import models
from StudentPerformancePrediction import models
from django.contrib.auth.models import User




def class_detail(request):
    data = models.StandardSection.objects.all()
    return render(request, 'class_detail.html', {"da": data})

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
        data = models.StandardSection(section=sec, standard_id=std)
        data.save()
        #return HttpResponseRedirect('/class_detail')
        return render(request, 'add_class.html')
    else:
        return render(request, 'add_class.html')


def delete_class(request, standard_section_id):
    if request.method == "POST":
        pi = models.StandardSection.objects.get(standard_section_id=standard_section_id)
        pi.delete()
        return HttpResponseRedirect('/class_detail.html')
        #return render(request, 'class_detail.html')

def get_teacher_prediction(request):
    stand = models.Standard.objects.all()
    if request.method == "GET":
        std = request.GET.get('Standard')
        # std = 12
        sec = models.StandardSection.objects.filter(standard=std)
        sub = models.TblSubject.objects.filter(standard=std)
        return render(request, 'teac_prediction.html', {'st': stand, 'se': sec, 'su': sub})


def get_prediction_data(request):
    pre_data = models.StudentEfficacy.objects.select_related('student_id__auth_user')
    prediction = pre_data.values('student_id__auth_user__username', 'predictions','student_id__auth_user__first_name','student_id__auth_user__last_name')
    return render(request, 'teac_prediction.html', {'pm': prediction})

    '''predicted_marks = models.StudentEfficacy.objects.select_related('student_id__auth_user', 'predictions')
#   data = models.MapMySchoolUserStandardSection.objects.filter()
    return render(request, 'teac_prediction.html', {'pm': predicted_marks})'''

'''def get_teacher_dashboard(request):
    a = views.student_navbar(request)
    return render(request, 'teac_dashboard.html', {'a': a})

def get_sub(request):'''

def get_prediction_principle(request):
    pre_data = models.StudentEfficacy.objects.select_related('student_id__auth_user')
    prediction = pre_data.values('student_id__auth_user__username', 'predictions','student_id__auth_user__first_name', 'student_id__auth_user__last_name')
    return render(request, 'prin_prediction.html', {'pm': prediction})
