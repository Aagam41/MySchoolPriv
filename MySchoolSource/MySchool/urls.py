"""MySchool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from MySchoolHome import urls as mshu
from StudentPerformance import urls as sp
from StudentFeedback import urls as sf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(mshu)),
    path('', include(sp)),
    path('', include(sf))
]

admin.site.site_header = "MySchool Administration"
admin.site.site_title = "MySchool Administration"
admin.site.index_title = "MySchool Administration"
admin.site.site_url = "http://127.0.0.1:8000/"
