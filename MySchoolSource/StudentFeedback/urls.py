from django.urls import path
from . import views

from aagam_packages.django.view_extensions import generic


app_name = "StudentFeedback"


urlpatterns = [
    path('student/feedback/home/', generic.ModelObjectListView.as_view(), name="student_feedback_home")
]


urlpatterns += [
    path('user_detail/', views.user_detail, name="user_detail"),
    path('login/', views.login, name="login"),
    path('add_user/', views.add_user, name="add_user"),
    path('edit_user/', views.edit_user, name="edit_user"),
    path('class_detail/', views.class_detail, name="class_detail"),
    path('edit_class/<int:standard_section_id>/', views.edit_class, name="edit_class"),
    path('add_class/', views.add_class, name="add_class"),
    path('delete_class/<int:standard_section_id>/', views.delete_class, name="delete_class"),
    path('get_teacher_prediction/', views.get_teacher_prediction, name='get_teacher_prediction'),
    path('get_prediction_data/', views.get_prediction_data, name='get_prediction_data'),
    path('get_prediction_principle', views.get_prediction_principle, name="get_prediction_principle")
    #path('get_teacher_dashboard/', views.get_teacher_dashboard, name='get_teacher_dashboard')
 ]
