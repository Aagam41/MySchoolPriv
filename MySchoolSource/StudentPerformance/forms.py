from django import forms
from .models import Student
from .models import TblClass

class StudentForm(forms.Form):
    person = forms.ModelChoiceField(queryset=Student.objects.values_list('person', flat=True),  empty_label=None)
    class_field = forms.ModelChoiceField(queryset=TblClass.objects.values_list('class_field',flat=True),  empty_label=None)

    class Meta:
        model = Student
        fields = ['person', 'class_field']