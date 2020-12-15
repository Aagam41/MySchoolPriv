from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views


from . import views

from aagam_packages.django_model_extensions.views import generic

app_name = 'MySchoolHome'

page_context = {'title': "MySchool Administration",
                'footerCreatedBy': '<a href="https://aagamsheth.com"/>Aagam Sheth.</a>'}

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(extra_context={'page_context': page_context, 'titleTag': 'Login'}),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(extra_context={'page_context': page_context, 'titleTag': 'Logout'}),
         name='logout'),
]

urlpatterns += [
    path('', views.home, name='home'),
    path('test/', views.test, name='test'),

    path('list/<str:app_label>/<str:model_label>/',
         generic.ModelObjectListView.as_view(extra_context={'page_context': {'titleTag': '1'}}),
         name='modelobject_list_view'),

    path('create/<str:app_label>/<str:model_label>/',
         generic.ModelObjectCreateView.as_view(extra_context={'page_context': {'titleTag': '1'}}),
         name='modelobject_create_view'),
    path('create/<str:app_label>/<str:model_label>/<str:template_label>/',
         generic.ModelObjectCreateView.as_view(), name='modelobject_create_view'),

    path('delete/<str:app_label>/<str:model_label>/<int:pk>/',
         generic.ModelObjectDeleteView.as_view(), name='modelobject_delete_view'),
    path('delete/<str:app_label>/<str:model_label>/<int:pk>/<str:template_label>/',
         generic.ModelObjectDeleteView.as_view(), name='modelobject_delete_view'),
    path('delete/<str:app_label>/<str:model_label>/<int:pk>/<str:template_label>/<str:success_label>/',
         generic.ModelObjectDeleteView.as_view(), name='modelobject_delete_view'),
]
