from django.urls import path

from . import views

app_name = 'StudentPerformance'

urlpatterns = [
    path('test/', views.paper_entry_create)
]
