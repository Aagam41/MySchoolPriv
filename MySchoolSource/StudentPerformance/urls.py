from django.urls import path
from . import views


urlpatterns = [
    path('subentry/', views.subject_entry),
    path('subdelete/', views.subject_delete),
    path('subupdate/', views.subject_update),
    path('chapentry/', views.chapter_entry),
    path('topicentry/', views.topic_entry),
    path('chapupdate/', views.chapter_update),
    path('chapdelete/', views.chapter_delete),
    path('topicupdate/', views.topic_update),
    path('topicdelete/', views.topic_delete),
]