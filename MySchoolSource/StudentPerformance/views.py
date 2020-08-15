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
def test(request):
    context = {
        'cardTitle': "Lowest Performance",
        'cardSubtitle': "Based on the Formative Assessment",
        'cardText': "Hello"
    }
    return render(request, 'Aagam/chart.html', context)