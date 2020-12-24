from django.urls import path

from . import views

app_name = 'StudentPerformance'

urlpatterns = [
    path('student-performance/<str:performance_type>', views.performance_panel, name="student_performance")
]
