from django.http import Http404, HttpResponse
from django.apps import apps
from django.template.exceptions import TemplateDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .models import *

from aagam_packages.terminal_yoda.terminal_yoda import *

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


class ModelObjectCreateView(CreateView):
    def __init__(self):
        super(ModelObjectCreateView, self).__init__()
        self.app_label = ""
        self.model_label = ""
        self.template_label = ""
        self.success_label = ""

    def dispatch(self, request, *args, **kwargs):
        self.model_label = kwargs.get('model_label', None)
        self.app_label = kwargs.get('app_label', None)
        self.model = apps.get_model(self.app_label, self.model_label.capitalize())
        self.fields = self.get_modelobject_fields_label()

        self.context_object_name = 'object'

        self.template_label = kwargs.get('template_label', None)
        self.template_name = self.get_template_name_label()
        try:
            ret = super(ModelObjectCreateView, self).dispatch(request, *args, **kwargs)
        except AttributeError:
            raise Http404
        return ret

    def get_template_name_label(self):
        if self.template_label == "0":
            template_name = f'{self.app_label}/{self.model_label}_create.html'
        elif self.template_label:
            template_name = self.template_name
        else:
            template_name = 'modelobject_create.html'
        return template_name

    def get_modelobject_fields_label(self):
        model_label = list()
        field_label = list()
        for app in apps.get_app_configs():
            for model in app.get_models():
                model_label.append(model._meta.verbose_name.replace(" ", ""))
        field_labels = self.model._meta.get_fields()
        for field in field_labels:
            if field.name == f'{self.model.objects.model._meta.db_table}_id':
                pass
            elif field.name in model_label:
                pass
            else:
                field_label.append(field.name)
        return field_label


class ModelObjectDeleteView(DeleteView):
    def __init__(self):
        super(ModelObjectDeleteView, self).__init__()
        self.app_label = ""
        self.model_label = ""
        self.template_label = ""
        self.success_label = ""

    def dispatch(self, request, *args, **kwargs):
        self.model_label = kwargs.get('model_label', None)
        self.app_label = kwargs.get('app_label', None)
        self.model = apps.get_model(self.app_label, self.model_label.capitalize())

        self.context_object_name = f'object'

        self.template_label = kwargs.get('template_label', None)
        self.template_name = self.get_template_name_label()

        self.success_label = kwargs.get('success_label', None)
        self.success_url = reverse_lazy(self.get_success_url_label())
        try:
            ret = super(ModelObjectDeleteView, self).dispatch(request, *args, **kwargs)
        except AttributeError:
            raise Http404
        except TemplateDoesNotExist:
            return HttpResponse(status=501)
        return ret

    def get_template_name_label(self):
        if self.template_label == "0":
            template_name = f'{self.app_label}/{self.model_label}_confirm_delete.html'
        elif self.template_label:
            template_name = self.template_name
        else:
            template_name = 'modelobject_confirm_delete.html'
        return template_name

    def get_success_url_label(self):
        if self.success_label == "0":
            success_url = f'{self.app_label}/{self.model_label}_success_url.html'
        elif self.success_label:
            yoda_saberize_print(self.success_label, YodaSaberColor.WHITE, YodaSaberColor.RED)
            success_url = self.success_label
        else:
            success_url = 'MySchoolHome:test'
        return success_url
