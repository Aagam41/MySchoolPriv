from django.http import Http404, HttpResponse
from django.apps import apps
from django.template.exceptions import TemplateDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .models import *

from aagam_packages.terminal_yoda.terminal_yoda import *
from aagam_packages.django_model_extensions.views import generic

# Create your views here.


class PaperTypeListView(ListView):
    model = PaperType
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PaperTypeUpdateView(UpdateView):
    model = PaperType
    fields = ['paper_type', 'out_of']


class PaperEntryListView(ListView):
    model = PaperEntry
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PaperEntryUpdateView(UpdateView):
    model = PaperEntry
    fields = ['paper_entry_name', 'subject', 'paper_type', 'paper_entry_date']


class cv(generic.ModelObjectCreateView):
    success_label = ""
