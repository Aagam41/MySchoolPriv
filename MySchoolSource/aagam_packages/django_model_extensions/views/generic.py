from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.apps import apps
from django.template.exceptions import TemplateDoesNotExist
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView


class ModelObjectCreateView(LoginRequiredMixin, CreateView):
    context_object_name = 'object'
    app_label = ""
    model_label = ""
    fields_label = ""
    template_label = ""
    success_label = ""

    def dispatch(self, request, *args, **kwargs):
        self.app_label = kwargs.get('app_label', None)
        self.model_label = kwargs.get('model_label', None)
        self.model = apps.get_model(self.app_label, self.model_label.capitalize())
        self.fields = self.get_modelobject_fields_label()

        self.template_label = kwargs.get('template_label', None)
        self.template_name = self.get_template_name_label()
        try:
            ret = super(ModelObjectCreateView, self).dispatch(request, *args, **kwargs)
        except AttributeError:
            raise Http404
        return ret

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_template_name_label(self):
        if self.template_label == "0":
            template_name = f'{self.app_label}/{self.model_label}_create.html'
        elif self.template_label:
            app1, page1 = self.template_label.split("-", 1)
            template_name = f'{app1}/{page1}.html'
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
            elif not field.editable:
                pass
            else:
                field_label.append(field.name)
        return field_label


class ModelObjectDeleteView(LoginRequiredMixin, DeleteView):
    context_object_name = f'object'
    app_label = ""
    model_label = ""
    template_label = ""
    success_label = ""

    def dispatch(self, request, *args, **kwargs):
        self.model_label = kwargs.get('model_label', None)
        self.app_label = kwargs.get('app_label', None)
        self.model = apps.get_model(self.app_label, self.model_label.capitalize())

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
            template_name = f'{self.template_label}.html'
        else:
            template_name = 'modelobject_confirm_delete.html'
        return template_name

    def get_success_url_label(self):
        if self.success_label == "0":
            success_url = f'{self.app_label}/{self.model_label}_success_url.html'
        elif self.success_label:
            success_url = self.success_label
        else:
            success_url = 'modelobject_success_url.html'
        return success_url
