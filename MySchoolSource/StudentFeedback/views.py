from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from StudentPerformance import models as sp
from MySchoolHome import views
from StudentFeedback import models
from StudentPerformancePrediction import models as spp
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Sum, Avg
import collections
import operator
import itertools
def class_detail(request):
    data = sp.StandardSection.objects.all()
    return render(request, 'class_detail.html', {"da": data})


def edit_class(request, standard_section_id):
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
    pre_data = spp.StudentEfficacy.objects.select_related('student_id__auth_user')
    prediction = pre_data.values('student_id__auth_user__username', 'predictions', 'student_id__auth_user__first_name','student_id__auth_user__last_name')
    marks = pre_data.filter(predictions__gt=75).values('predictions').count()
    pmarks = pre_data.filter(predictions__gt=45, predictions__lt=75).values('predictions').count()
    lmarks = pre_data.filter(predictions__gt=23, predictions__lt=45).values('predictions').count()
    fail = pre_data.filter(predictions__lt=23).values('predictions').count()
    d = [marks, pmarks, lmarks, fail]
    return render(request, 'teac_prediction.html', {'pm': prediction, 'd': d})





def graph_teacher_dashboard(user_id):
    sub = "Mathematics 9709"

    data = sp.MapStudentPaperPatternEntry.objects.select_related('paper_pattern_entry').\
        filter(myschool_user=user_id,
               paper_pattern_entry__paper_entry__paper_type__paper_type__contains="Assignment")
    marks = data.filter(
        paper_pattern_entry__paper_question__chapter_topic__subject_chapter__subject__subject_name=sub)
    am = list(marks.values_list('marks_obtained', flat=True))
    actual_marks = sum(am)
    dic = {
        user_id: actual_marks,
    }
    return dic

def Overall_class_performance(paperType):
    sub = "Mathematics 9709"
    data = sp.MapStudentPaperPatternEntry.objects.select_related('paper_pattern_entry').\
        filter(paper_pattern_entry__paper_entry__paper_type__paper_type__contains=paperType)
    marks = data.filter(
        paper_pattern_entry__paper_question__chapter_topic__subject_chapter__subject__subject_name=sub)
    actual_marks = marks.aggregate(Avg('marks_obtained'))
    return actual_marks


def get_teacher_dashboard(request):
   data = sp.MapStudentPaperPatternEntry.objects.select_related('myschool_user_id__auth_user')
   tp = data.filter(marks_obtained__gt=21).values('myschool_user_id__auth_user__username')
   pp = data.filter(marks_obtained__gt=15).values('myschool_user_id__auth_user__username')
   lp = data.filter(marks_obtained__lte=15).values('myschool_user_id__auth_user__username')
   userId=list(sp.MapStudentPaperPatternEntry.objects.values_list('myschool_user_id', flat=True).distinct())
   minMarks={}
   for i in userId:
        minMarks.update(graph_teacher_dashboard(i))
   minMarks_values = sorted(minMarks.values())  # Sort the values
   sorted_minMarks = {}

   for i in minMarks_values:
       for k in minMarks.keys():
           if minMarks[k] == i:
               sorted_minMarks[k] = minMarks[k]
               break
   sorted_Keys=(list(sorted_minMarks.keys()))
   uname= sp.MySchoolUser.objects.select_related('auth_user').values('auth_user__username')
   actual_user = []
   for i in sorted_Keys:
        actual_user.append(list(uname.values_list('auth_user__username', flat=True).filter(myschool_user_id=i)))
   sorted_user= list(itertools.chain.from_iterable(actual_user))[:10]
   sorted_values= (list(sorted_minMarks.values()))[:10]
   unit_Marks = Overall_class_performance("Unit Test")
   mid_sem = Overall_class_performance("Mid Sem")
   assignments = Overall_class_performance("Assignment")
   practical = Overall_class_performance("Practical")
   return render(request, 'teac_dashboard.html', {'t': tp, 'p': pp, 'l': lp,
                                                  'user': sorted_user,
                                                  'values': sorted_values,
                                                  'Unit_Marks': unit_Marks,
                                                  'Mid_Marks': mid_sem,
                                                  'Assignment': assignments,
                                                  'Practical': practical, })

def stu_dashboard(request):
    return render(request, 'stu_dashboard.html')

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
        father_education = request.POST["Father_education"]
        internet_facility = request.POSt["Internet_Facility"]
        study_time = request.POST["Study_Time"]
        paid_tuition = request.POST["Paid_Tution"]
        past_failures = request.POST["Past_Failures"]
        free_time = request.POST["Free_Time"]
        extra_curricular_activities = request.POST["Extra_Curricular_activites"]
        health = request.POST["Health"]
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

