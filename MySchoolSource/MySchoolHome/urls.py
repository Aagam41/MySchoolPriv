from django.urls import path
from django.contrib.auth import views as auth_views


from . import views

from aagam_packages.django.view_extensions import generic

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
    path('test/', views.test, name='test'),
    path('sitemap/', views.sitemap, name='sitemap'),
]


urlpatterns += [
    path('', views.home, name='home'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('educator/', views.educator_dashboard, name='educator_dashboard'),
    path('principal/', views.principal_dashboard, name='principal_dashboard'),
]


urlpatterns += [

    path('list/<str:app_label>/<str:model_label>/',
         generic.ModelObjectListView.as_view(extra_context={'page_context': {'titleTag': '1'}}),
         name='modelobject_list_view'),
    path('list/<str:app_label>/<str:model_label>/<str:template_label>/',
         generic.ModelObjectListView.as_view(), name='modelobject_list_view'),

    path('create/<str:app_label>/<str:model_label>/',
         generic.ModelObjectCreateView.as_view(extra_context={'page_context': {'titleTag': '1'}}),
         name='modelobject_create_view'),
    path('create/<str:app_label>/<str:model_label>/<str:template_label>/',
         generic.ModelObjectCreateView.as_view(), name='modelobject_create_view'),

    path('update/<str:app_label>/<str:model_label>/<int:pk>/',
         generic.ModelObjectUpdateView.as_view(), name='modelobject_update_view'),
    path('update/<str:app_label>/<str:model_label>/<int:pk>/<str:template_label>/',
         generic.ModelObjectUpdateView.as_view(), name='modelobject_update_view'),

    path('delete/<str:app_label>/<str:model_label>/<int:pk>/',
         generic.ModelObjectDeleteView.as_view(), name='modelobject_delete_view'),
    path('delete/<str:app_label>/<str:model_label>/<int:pk>/<str:template_label>/',
         generic.ModelObjectDeleteView.as_view(), name='modelobject_delete_view'),
    path('delete/<str:app_label>/<str:model_label>/<int:pk>/<str:template_label>/<str:success_label>/',
         generic.ModelObjectDeleteView.as_view(), name='modelobject_delete_view'),
]
