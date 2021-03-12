from django.shortcuts import render

from StudentPerformancePrediction import models as spp
from . import models


# region Bhavesh

def get_prediction_data(request):
    pre_data = models.StudentEfficacy.objects.select_related('student_id__auth_user')
    prediction = pre_data.values('student_id__auth_user__username', 'predictions', 'student_id__auth_user__first_name','student_id__auth_user__last_name')
    marks = pre_data.filter(predictions__gt=75).values('predictions').count()
    pmarks = pre_data.filter(predictions__gt=45, predictions__lt=75).values('predictions').count()
    lmarks = pre_data.filter(predictions__gt=23, predictions__lt=45).values('predictions').count()
    fail = pre_data.filter(predictions__lt=23).values('predictions').count()
    d = [marks, pmarks, lmarks, fail]
    return render(request, 'teac_prediction.html', {'pm': prediction, 'd': d})


def student_prediction(request):
    return render(request, 'stu_prediction.html')


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
# endregion
