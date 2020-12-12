from django.http import Http404
from django.apps import apps
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


class PaperEntryListView(ListView):
    model = PaperEntry
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PaperEntryCreateView(CreateView):
    model = PaperEntry
    fields = ['paper_entry_name', 'subject', 'paper_type', 'paper_entry_date']


class PaperEntryUpdateView(UpdateView):
    model = PaperEntry
    fields = ['paper_entry_name', 'subject', 'paper_type', 'paper_entry_date']


class PaperEntryDeleteView(DeleteView):
    model = PaperEntry
    success_url = reverse_lazy('MySchoolHome:test')


class ModelObjectDeleteView(DeleteView):
    context_object_name = 'object'
    template_name = 'StudentPerformance/model_object_confirm_delete.html'
    success_url = reverse_lazy('MySchoolHome:test')

    def dispatch(self, request, *args, **kwargs):
        model_label = kwargs.get('model_label', None)
        app_label = kwargs.get('app_label', None)
        self.model = apps.get_model(app_label, model_label.capitalize())
        try:
            ret = super(ModelObjectDeleteView, self).dispatch(request, *args, **kwargs)
        except AttributeError:
            raise Http404
        return ret
