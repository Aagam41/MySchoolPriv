from django.shortcuts import render
from StudentFeedback.models import *
from MySchoolHome.models import *
from StudentPerformance.models import *
# Create your views here.

def form_list(request):
    if request.method == "POST":
        data = FeedbackFormQuestion.yash_objects.retrive_feedback_forms()
        rate = request.POST['rate']
        com = request.POST['com']
        try:
            user_id = '1'
            r_c = Feedback.yash_objects.retrive_feedback_forms(rate=rate, com=com, user_id=user_id)
        except:
            print('Some Error occured')
        context = {
            'username':data.feedback_form.subject_teacher.myschool_user.auth_user.username,
            'subject':data.feedback_form.subject_teacher.subject.subject_name,
            'status':data.feedback_form.feedback_form_status,
            'question':data.feedback_question.question_text,
        }
        return render(request, 'feedback.html', context, data, r_c)
    else:
        return render(request, 'feedback.html')
'''
{% for d in data %}
{% if d.feedback_form.feedback_form_status %}
<p> <b> {{ d.feedback_form.subject_teacher.myschool_user.auth_user.username }} </b> 
<i> {{ d.feedback_form.subject_teacher.subject.subject_name }} </i>
<u> {{ d.feedback_form.feedback_form_status }} </u> 
<b> {{d.feedback_question.question_text}} </b> 
</p>
{% endif %}
{% endfor %}
<p>
{{ subject.subject_name }}
{{ f[0].feedback_form_question.feedback_form.subject_teacher.subject.subject_name }}
{{ a = Feedback.yash_objects.map_teacher_subject("Mathematics 9709") }}
</p>
'''

'''
for x in t:
...     print(x.feedback_form_question.feedback_form.subject_teacher.subject.subject_name)
'''


def teacher_feedback(request):
    user_id = 27
    myschool_user = MySchoolUser.objects.get(auth_user=User.objects.get(id=user_id))
    map = MapMySchoolUserSubject.objects.filter(myschool_user=myschool_user)
    rate = {}
    com = {}
    for t in map:
        t_data = Feedback.yash_objects.map_teacher_subject(t.subject.subject_name)
        rate[t.subject.subject_name] = 0
        com[t.subject.subject_name] = []
        for x in t_data:
            rate[t.subject.subject_name] += int(x[0].feedback_rating)
            com[t.subject.subject_name].append(x[0].feedback_comments)
    return render(request, '', {'t_data': t_data, 'rate': rate, 'com': com})

def feedback_principal(request):
    f = Feedback.yash_objects.all()
    # f[0].feedback_form_question.feedback_form.subject_teacher.myschool_user.auth_user.username = Teacher name
    # for t in f:
    # ...     print(t.feedback_rating) = Feedback rating according to teacher
    return f

