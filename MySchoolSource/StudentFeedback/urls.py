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
    path('add_class/', views.add_class, name="add_class"),
    path('edit_class/', views.edit_class, name="edit_class"),
    path('subject_detail/', views.subject_detail, name="subject_detail"),
    path('add_subject/', views.add_subject, name="add_subject"),
    path('edit_subject/', views.edit_subject, name="edit_subject"),
    path('chapter_detail/', views.chapter_detail, name="chapter_detail"),
    path('add_chapter/', views.add_chapter, name="add_chapter"),
    path('edit_chapter/', views.edit_chapter, name="edit_chapter"),
    path('topic_detail/', views.topic_detail, name="topic_detail"),
    path('add_topic/', views.add_topic, name="add_topic"),
    path('edit_topic/', views.edit_topic, name="edit_topic"),
    path('teac_dashboard/', views.teac_dashboard, name="teac_dashboard"),
    path('teac_prediction/', views.teac_prediction, name="teac_prediction"),
    path('teac_feedback/', views.teac_feedback, name="teac_feedback"),
    path('stu_prediction/', views.stu_prediction, name="stu_prediction"),
    path('stu_dashboard/', views.stu_dashboard, name="stu_dashboard"),
    path('stu_feedback/', views.stu_feedback, name="stu_feedback"),
    path('prin_dashboard/', views.prin_dashboard, name="prin_dashboard"),
    path('prin_feedback/', views.prin_feedback, name="prin_feedback"),
    path('prin_prediction/', views.prin_prediction, name="prin_prediction"),
    path('prediction_data/', views.prediction_data, name="prediction_data"),
]