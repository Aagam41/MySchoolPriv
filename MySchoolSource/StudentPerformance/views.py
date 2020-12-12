from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .models import *
from .forms import *

# Create your views here.


class PaperTypeListView(ListView):
    model = PaperType
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PaperTypeCreateView(CreateView):
    model = PaperType
    fields = ['paper_type', 'out_of']


class PaperTypeUpdateView(UpdateView):
    model = PaperType
    fields = ['paper_type', 'out_of']


class PaperTypeDeleteView(DeleteView):
    model = PaperType
    success_url = reverse_lazy('MySchoolHome:test')
