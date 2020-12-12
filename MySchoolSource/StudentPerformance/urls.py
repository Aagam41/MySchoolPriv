from django.urls import path

from . import views

app_name = 'StudentPerformance'

urlpatterns = [
    path('paper-type-form/list', views.PaperTypeListView.as_view(), name='papertype_list_view'),
    path('paper-type-form/create', views.PaperTypeCreateView.as_view(), name='papertype_create_view'),
    path('paper-type-form/update/<int:pk>', views.PaperTypeUpdateView.as_view(), name='papertype_update_view'),
    path('paper-type-form/delete/<int:pk>', views.PaperTypeDeleteView.as_view(), name='papertype_delete_view'),

    path('paper-entry-form/list', views.PaperEntryListView.as_view(), name='paperentry_list_view'),
    path('paper-entry-form/create', views.PaperEntryCreateView.as_view(), name='paperentry_create_view'),
    path('paper-entry-form/update/<int:pk>', views.PaperEntryUpdateView.as_view(), name='paperentry_update_view'),
    path('paper-entry-form/delete/<int:pk>', views.PaperEntryDeleteView.as_view(), name='paperentry_delete_view'),

    path('paper-entry-form/delete1/<str:app_label>/<str:model_label>/<int:pk>', views.ModelObjectDeleteView.as_view(), name='model-object_delete_view'),
]
