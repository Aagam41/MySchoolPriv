from django.urls import path

from . import views

app_name = 'StudentPerformance'

urlpatterns = [
    path('paper-type-form/list', views.PaperTypeListView.as_view(), name='papertype_list_view'),
    path('paper-type-form/update/<int:pk>', views.PaperTypeUpdateView.as_view(), name='papertype_update_view'),
    path('paper-entry-form/list', views.PaperEntryListView.as_view(), name='paperentry_list_view'),
    path('paper-entry-form/update/<int:pk>', views.PaperEntryUpdateView.as_view(), name='paperentry_update_view'),
]
