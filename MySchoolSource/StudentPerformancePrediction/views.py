from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .models import StudentEfficacy
from StudentPerformance.models import PaperType
from MySchoolHome.models import MySchoolUser

from MySchoolHome import views
from .MachineLearningModels import LinearRegression

# Create your views here.


def student_prediction(request):
    prediction_data = StudentEfficacy.objects.get(student=MySchoolUser.objects.get(auth_user=request.user))

    father_education = ""
    internet_facility = ""
    study_time = ""
    paid_tuition = ""
    past_failures = ""
    free_time = ""
    extra_curricular_activities = ""
    absences = ""
    class_engagement = ""
    health = ""

    if prediction_data.father_education == 0:
        father_education = "No education"
    elif prediction_data.father_education == 1:
        father_education = "Primary Education"
    elif prediction_data.father_education == 2:
        father_education = "Secondary Education"
    elif prediction_data.father_education == 3:
        father_education = "Graduate Study"
    elif prediction_data.father_education == 4:
        father_education = "Post Graduate Study"
    elif prediction_data.father_education == 5:
        father_education = "Doctor of Philosophy"

    if prediction_data.internet_facility == 0:
        internet_facility = "Not Available"
    elif 2 < prediction_data.internet_facility == 1:
        internet_facility = "Available"

    study_time = prediction_data.study_time

    if prediction_data.paid_tuition == 0:
        paid_tuition = "None"
    elif 2 < prediction_data.paid_tuition == 1:
        paid_tuition = "Yes"

    past_failures = prediction_data.past_failures

    free_time = prediction_data.free_time

    if prediction_data.extra_curricular_activities == 0:
        extra_curricular_activities = "None"
    elif 2 < prediction_data.extra_curricular_activities == 1:
        extra_curricular_activities = "Yes"

    absences = prediction_data.absences

    if prediction_data.class_engagement == 1:
        class_engagement = "No Engagement"
    elif prediction_data.class_engagement == 2:
        class_engagement = "Only When Asked"
    elif prediction_data.class_engagement == 3:
        class_engagement = "Rarely Engaged"
    elif prediction_data.class_engagement == 4:
        class_engagement = "Engaging Often"
    elif prediction_data.class_engagement == 5:
        class_engagement = "Highly Engaged"

    if prediction_data.health == 1:
        health = "Not Healthy"
    elif prediction_data.health == 2:
        health = "Not Fit"
    elif prediction_data.health == 3:
        health = "Sick"
    elif prediction_data.health == 4:
        health = "Good Health"
    elif prediction_data.health == 5:
        health = "At the Pink of Health"

    predicted_marks = LinearRegression.fetch_prediction_data(MySchoolUser.objects.get(auth_user=request.user))

    total_marks = PaperType.objects.get(paper_type="Final Exam")
    total_marks = total_marks.out_of

    percentage = (predicted_marks / total_marks) * 100

    context = {'page_context': {'title': "MySchool Student Dashboard", 'titleTag': 'MySchool'},
               'search_name': '',
               'navbar': views.student_navbar(request),
               'prediction': {
                    'father_education': father_education,
                    'internet_facility': internet_facility,
                    'study_time': study_time,
                    'paid_tuition': paid_tuition,
                    'past_failures': past_failures,
                    'free_time': free_time,
                    'extra_curricular_activities': extra_curricular_activities,
                    'absences': absences,
                    'class_engagement': class_engagement,
                    'health': health,
                    'predicted_marks': predicted_marks,
                    'total_marks': total_marks,
                    'percentage': percentage
               }}
    return render(request, 'StudentPerformancePrediction/student_prediction.html', context)
