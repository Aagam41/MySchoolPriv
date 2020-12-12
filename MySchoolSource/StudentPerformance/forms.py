from django import forms
from django.forms import ModelForm

from .models import *


class PaperTypeForm(ModelForm):
    class Meta:
        model = PaperType
        fields = ['paper_type', 'out_of']