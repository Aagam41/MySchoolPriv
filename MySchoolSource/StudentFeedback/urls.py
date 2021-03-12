from django.urls import path

from StudentFeedback import views

app_name = "StudentFeedback"


urlpatterns = [
    path('student/feedback/home/', views.feedback_panel, name="student_feedback_home"),
    path('student/add_feedback/', views.add_feedback, name="add_feedback")
]
