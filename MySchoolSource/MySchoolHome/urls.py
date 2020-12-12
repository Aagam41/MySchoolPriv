from django.urls import path, include
from django.conf.urls import url

from . import views

app_name = 'MySchoolHome'

urlpatterns = [
    path('', views.test, name='test'),
    path('login/', views.msh_login_page, name="msh_login_page")
]