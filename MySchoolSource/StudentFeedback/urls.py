from django.urls import path
from . import views

from aagam_packages.django.view_extensions import generic


app_name = "StudentFeedback"


urlpatterns = [
    path('student/feedback/home/', generic.ModelObjectListView.as_view(), name="student_feedback_home")
]


urlpatterns += [
    path('class_detail/', views.class_detail, name="class_detail"),
    path('edit_class/<int:standard_section_id>/', views.edit_class, name="edit_class"),
    path('add_class/', views.add_class, name="add_class"),
    path('delete_class/<int:standard_section_id>/', views.delete_class, name="delete_class"),
    path('get_prediction_data/', views.get_prediction_data, name='get_prediction_data'),
    path('get_teacher_dashboard/', views.get_teacher_dashboard, name='get_teacher_dashboard'),
    path('student_prediction/',views.student_prediction, name='student_prediction'),
    path('test/', views.test, name='test'),
    path('pr_dashboard', views.pr_dashboard, name='pr_dashboard'),
    path('student_data_prediction' , views.student_data_prediction , name='student_data_prediction'),
    path('stu_dashboard', views.stu_dashboard, name='stu_dashboard'),
    path('graph_teacher_dashboard', views.graph_teacher_dashboard, name='graph_teacher_dashboard')
]