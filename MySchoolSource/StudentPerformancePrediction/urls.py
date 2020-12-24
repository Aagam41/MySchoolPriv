from django.urls import path
from . import views

from aagam_packages.django.view_extensions import generic


app_name = "StudentPerformancePrediction"


urlpatterns = [
    path('student/prediction/<int:id>/', views.student_prediction, name="student_prediction")
]

