import os
import json
from django.contrib.auth.models import User

from MySchool import settings
from MySchoolHome import models as msh
from StudentPerformance import models as sp
from StudentFeedback import models as sf
from StudentPerformancePrediction import models as spp


with open('C:\Users\gvp\PycharmProjects\MySchoolPriv\MySchoolSource\JsonData\Latest\user.json') as f:
    user = json.load(f)


for p in user:
    p = User(username=p['username'], password=p['password'], first_name=p['first_name'], last_name=p['last_name'],
             email=p['email'], groups=p['groups'])
    p.save()


# for s in student:
#     s = Student(person=Person.objects.get(pk=s['person']), class_field=TblClass.objects.get(pk=s['class_field']))
#     s.save()

