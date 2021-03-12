from django.urls import path

from . import views

app_name = "StudentPerformancePrediction"


urlpatterns = [
    path('student/prediction', views.student_prediction, name="student_prediction")
]
