from django.urls import path

from . import views

from aagam_packages.django_model_extensions.views import generic

app_name = 'StudentPerformance'

urlpatterns = [
    path('paper-type-form/list', views.PaperTypeListView.as_view(), name='papertype_list_view'),
    path('paper-type-form/update/<int:pk>', views.PaperTypeUpdateView.as_view(), name='papertype_update_view'),
    path('paper-entry-form/list', views.PaperEntryListView.as_view(), name='paperentry_list_view'),
    path('paper-entry-form/update/<int:pk>', views.PaperEntryUpdateView.as_view(), name='paperentry_update_view'),

    path('create/<str:app_label>/<str:model_label>',
         generic.ModelObjectCreateView.as_view(), name='model-object_create_view'),
    path('create/<str:app_label>/<str:model_label>/<str:template_label>/',
         generic.ModelObjectCreateView.as_view(), name='model-object_create_view'),

    path('delete/<str:app_label>/<str:model_label>/<int:pk>',
         generic.ModelObjectDeleteView.as_view(), name='model-object_delete_view'),
    path('delete/<str:app_label>/<str:model_label>/<int:pk>/<str:template_label>',
         generic.ModelObjectDeleteView.as_view(), name='model-object_delete_view'),
    path('delete/<str:app_label>/<str:model_label>/<int:pk>/<str:template_label>/<str:success_label>',
         generic.ModelObjectDeleteView.as_view(), name='model-object_delete_view'),
]
