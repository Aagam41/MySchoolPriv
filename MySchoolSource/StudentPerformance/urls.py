from django.urls import path

from . import views

app_name = 'StudentPerformance'

urlpatterns = [
    path('paper-type-form/list', views.PaperTypeListView.as_view(), name='papertype_list_view'),
    path('paper-type-form/create', views.PaperTypeCreateView.as_view(), name='papertype_create_view'),
    path('paper-type-form/update/<int:pk>', views.PaperTypeUpdateView.as_view(), name='papertype_update_view'),
    path('paper-type-form/delete/<int:pk>', views.PaperTypeDeleteView.as_view(), name='papertype_delete_view'),
]

