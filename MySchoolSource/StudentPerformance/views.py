from django.shortcuts import render, redirect

from .models import *
from .forms import *

# Create your views here.


def paper_type_creation_form_page(request, edit, paper_type_id):
    if request.method == "POST":
        if edit:
            inst = PaperType.objects.get(pk=paper_type_id)
            paper_type_form = PaperTypeForm(data=request.POST, instance=inst)
            if paper_type_form.is_valid():
                return redirect('MySchoolHome:test')
        else:
            paper_type_form = PaperTypeForm(data=request.POST)
            if paper_type_form.is_valid():
                return redirect('MySchoolHome:test')
    else:
        if edit:
            inst = PaperType.objects.get(pk=paper_type_id)
            paper_type_form = PaperTypeForm(instance=inst)
        else:
            paper_type_form = PaperTypeForm()

    return render(request, 'StudentPerformance/paper_type_form.html', {'form': paper_type_form})
