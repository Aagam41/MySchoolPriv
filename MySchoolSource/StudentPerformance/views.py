from django.views.generic import ListView, UpdateView

from .models import *

from aagam_packages.django.view_extensions import generic


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
