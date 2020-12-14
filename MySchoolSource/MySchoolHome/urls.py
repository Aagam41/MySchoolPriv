from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views


from . import views

from aagam_packages.django_model_extensions.views import generic

app_name = 'MySchoolHome'

urlpatterns = [
    url('login/', auth_views.LoginView.as_view(), name='login'),
    url('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

urlpatterns += [
    path('', views.test, name='test'),

    path('create/<str:app_label>/<str:model_label>/',
         login_required(generic.ModelObjectCreateView.as_view()), name='modelobject_create_view'),
    path('create/<str:app_label>/<str:model_label>/<str:template_label>/',
         generic.ModelObjectCreateView.as_view(), name='modelobject_create_view'),
    path('create/<str:app_label>/<str:model_label>/<str:template_label>/<str:form_class>',
         generic.ModelObjectCreateView.as_view(), name='modelobject_create_view'),

    path('delete/<str:app_label>/<str:model_label>/<int:pk>/',
         generic.ModelObjectDeleteView.as_view(), name='modelobject_delete_view'),
    path('delete/<str:app_label>/<str:model_label>/<int:pk>/<str:template_label>/',
         generic.ModelObjectDeleteView.as_view(), name='modelobject_delete_view'),
    path('delete/<str:app_label>/<str:model_label>/<int:pk>/<str:template_label>/<str:success_label>/',
         generic.ModelObjectDeleteView.as_view(), name='modelobject_delete_view'),
]
