from django.urls import path
from . import views

urlpatterns = [
    path('user_detail/', views.user_detail, name="user_detail"),
    path('add_user/', views.add_user, name="add_user"),
    path('edit_user/', views.edit_user, name="edit_user"),
    path('class_detail/', views.class_detail, name="class_detail"),
    #path('edit_class/', views.edit_class, name="edit_class"),
    path('add_class/', views.add_class, name="add_class"),
    path('delete_class/<int:standard_section_id>/', views.delete_class, name="delete_class")
 ]
