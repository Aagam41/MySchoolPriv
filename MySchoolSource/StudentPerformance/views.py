from django.shortcuts import render
from django.http import HttpResponse
from .forms import StudentForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        form.save()
    else:
        form = StudentForm()
    return render(request, 'StudentPerformance/Registration.html', {'form': form})