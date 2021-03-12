from django.shortcuts import render
from MySchoolHome import views as mshv
from django.shortcuts import render

from MySchoolHome import views as mshv


# Create your views here.
def feedback_panel(request):
    if request.user.groups.filter(name='Learner').exists():
        navbar = mshv.student_navbar(request)
        user = "learner"
        context = {
            'navbar': navbar,
            'user_group': user,
        }
        return render(request, 'StudentFeedback/feedback.html', context)
    elif request.user.groups.filter(name='Educator').exists():
        educator_context = mshv.educator_navbar(request)
        user = "educator"
        context = {
            'navbar': educator_context,
            'user_group': user,
        }
        return render(request, 'StudentFeedback/feedback.html', context)
    elif request.user.groups.filter(name='Principal').exists():
        navbar = mshv.principal_navbar()
        user = "principal"
        context = {
            'navbar': navbar,
            'user_group': user,
        }
        return render(request, 'StudentFeedback/feedback.html', context)

def add_feedback(request):
    return render(request, 'StudentFeedback/add_feedback.html')






