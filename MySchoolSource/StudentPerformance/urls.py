from django.urls import path

from . import views

app_name = 'StudentPerformance'


# region Aagam Sheth
urlpatterns = [
    path('student-performance/<str:performance_type>', views.performance_panel, name="student_performance"),
]
# endregion

# region Bhavesh
urlpatterns += [
    path('student-performance-list/<str:performance_type>', views.student_performance, name="stu_performance"),
    path('class_detail/', views.class_detail, name="class_detail"),
    path('edit_class/<int:standard_section_id>/', views.edit_class, name="edit_class"),
    path('add_class/', views.add_class, name="add_class"),
    path('delete_class/<int:standard_section_id>/', views.delete_class, name="delete_class"),
]
# endregion