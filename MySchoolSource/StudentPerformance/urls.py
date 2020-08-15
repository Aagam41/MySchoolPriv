from django.urls import path
from . import views

urlpatterns = [
    path('/reg', views.index, name="HomeRoute"),
    path('', views.test)
]
