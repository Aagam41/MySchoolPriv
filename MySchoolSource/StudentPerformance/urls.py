from django.urls import path

from . import views


app_name = 'StudentPerformance'

urlpatterns = [
    path('paper-type-form', views.paper_type_creation_form_page, name='sp_paper_type_creation_form_page'),
    path('paper-type-form/edit<bool:edit>/type<int:paper_type_id>', views.paper_type_creation_form_page, name='sp_paper_type_creation_form_page'),
]

