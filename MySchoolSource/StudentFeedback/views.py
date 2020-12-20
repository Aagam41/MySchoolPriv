from django.shortcuts import render
from StudentFeedback.models import *
# Create your views here.

def form_list(request):
    data = FeedbackFormQuestion.objects.retrive_feedback_forms()
    return render(request, '', {'data': data})

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
</p>
'''

