from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from StudentPerformance import models as sp
from MySchoolHome import views
from StudentFeedback import models
from StudentPerformancePrediction import models as spp
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Avg

def class_detail(request):
    data = sp.StandardSection.objects.all()
    return render(request, 'class_detail.html', {"da": data})


def edit_class(request, standard_section_id):
    '''if request.method == 'POST':
        standard_section_id = models.StandardSection.objects.get(pk=standard_section_id)
        std = request.POST["Standard"]
        sec = request.POST["Section"]
        data = models.StandardSection(section=sec, standard_id=std, instance=standard_section_id)
        data.save()'''
    std = [1]
    sec = ['A']
    standard_sec = sp.StandardSection.objects.get(pk=standard_section_id)
    return render(request, 'edit_class.html', {'st_se': standard_sec, 'st': std, 'se': sec})


def add_class(request):
    if request.method == 'POST':
        std = request.POST["Standard"]
        sec = request.POST["Section"]
        data = sp.StandardSection(section=sec, standard_id=std)
        data.save()
        # return HttpResponseRedirect('/class_detail')
        return render(request, 'add_class.html')
    else:
        return render(request, 'add_class.html')


def delete_class(request, standard_section_id):
    if request.method == "POST":
        pi = sp.StandardSection.objects.get(standard_section_id=standard_section_id)
        pi.delete()
        return HttpResponseRedirect('/class_detail.html')
        # return render(request, 'class_detail.html')

def get_prediction_data(request):
    pre_data = models.StudentEfficacy.objects.select_related('student_id__auth_user')
    prediction = pre_data.values('student_id__auth_user__username', 'predictions', 'student_id__auth_user__first_name','student_id__auth_user__last_name')
    marks = pre_data.filter(predictions__gt=75).values('predictions').count()
    pmarks = pre_data.filter(predictions__gt=45, predictions__lt=75).values('predictions').count()
    lmarks = pre_data.filter(predictions__gt=23, predictions__lt=45).values('predictions').count()
    fail = pre_data.filter(predictions__lt=23).values('predictions').count()
    d = [marks, pmarks, lmarks, fail]
    return render(request, 'teac_prediction.html', {'pm': prediction, 'd': d})


def get_teacher_dashboard(request):
   data = sp.MapStudentPaperPatternEntry.objects.select_related('myschool_user_id__auth_user')
   tp = data.filter(marks_obtained__gt=21).values('myschool_user_id__auth_user__username')
   pp = data.filter(marks_obtained__gt=15).values('myschool_user_id__auth_user__username')
   lp = data.filter(marks_obtained__lte=15).values('myschool_user_id__auth_user__username')
   da = sp.MapStudentPaperPatternEntry.objects.select_related('myschool_user_id__auth_user')
   marks = da.values('marks_obtained', 'myschool_user_id__auth_user__username').order_by('marks_obtained')
   mid_sem = sp.MapStudentPaperPatternEntry.objects.aggregate(Avg('marks_obtained'))
   #assignmnet = sp.MapStudentPaperPatternEntry.objects.select_related('paper_entry_id___paper_pattern_entry')
   #an = assignmnet.select_related('paper_entry_id__paper_entry')
   #r = an.filter(paper_type_id=1).values('paper_entry_name')
   all_data = sp.MapStudentPaperPatternEntry.objects.select_related(' paper_pattern_entry__p')
   assignment_marks = []
   practical_marks = []
   unit_test_marks = [] # filter used by 
   return render(request, 'teac_dashboard.html', {'t': tp, 'p': pp, 'l': lp, 'marks': marks, 'b': mid_sem})

def test(request):
    da = sp.MapStudentPaperPatternEntry.objects.select_related('myschool_user_id__auth_user')
    marks = da.values('marks_obtained', 'myschool_user_id__auth_user__username')
    return render(request, 'test.html', {'marks': marks})

def student_prediction(request):
    return render(request, 'stu_prediction.html')

def pr_dashboard(request):
    return render(request, 'prin_performance.html')

def student_data_prediction(request):
    if request.method == 'POST':
        father_education = request.POST["Father education :"]
        internet_facility = request.POSt["Internet Facility :"]
        study_time = request.POST[" Study Time "]
        paid_tuition = request.POST["Paid Tution :"]
        past_failures = request.POST["Past Failures :"]
        free_time = request.POST["Free Time :"]
        extra_curricular_activities = request.POST["Number of Extra Curricular Activites : "]
        health = request.POST["Health Issues :"]
        data = spp.StudentEfficacy(father_education=father_education,
                                   internet_facility=internet_facility,
                                   study_time=study_time,
                                   paid_tuition=paid_tuition,
                                   past_failures=past_failures,
                                   free_time=free_time,
                                   extra_curricular_activities=extra_curricular_activities,
                                   health=health)
        data.save()
        print("data is gone to database")
        # return HttpResponseRedirect('/class_detail')
        return render(request, 'add_class.html')
    else:
        return render(request, 'prediction_data.html')

