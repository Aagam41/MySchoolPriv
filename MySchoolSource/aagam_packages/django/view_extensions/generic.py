from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404, HttpResponse
from django.apps import apps
from django.template.exceptions import TemplateDoesNotExist
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth import views as auth_views


class ModelObjectListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    context_object_name = 'object'
    app_label = ""
    model_label = ""
    template_label = ""

    def dispatch(self, request, *args, **kwargs):
        self.app_label = kwargs.get('app_label', None)
        self.model_label = kwargs.get('model_label', None)
        self.model = apps.get_model(self.app_label, self.model_label.capitalize())

        self.template_label = kwargs.get('template_label', None)
        self.template_name = self.get_template_name_label()
        self.permission_required = self.get_permissions_required_label()
        try:
            ret = super(ModelObjectListView, self).dispatch(request, *args, **kwargs)
        except AttributeError:
            raise Http404
        return ret

    def get_queryset(self):
        filters = {}
        for key, value in self.request.GET.items():
            if value != '':
                filters[f'{key}__icontains'] = value
        filter_list = self.model.objects.filter(**filters)
        return filter_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = [
            field for field in self.get_modelobject_fields_label()
        ]
        context['display_fields'] = [
            field.replace('_', ' ').title() for field in self.get_modelobject_fields_label()
        ]
        return context

    def get_modelobject_fields_label(self, form1=None):
        model_label = list()
        field_label = list()
        display_field_label = list()
        for app in apps.get_app_configs():
            for model in app.get_models():
                model_label.append(model._meta.verbose_name.replace(" ", ""))
        field_labels = self.model._meta.get_fields()
        for field in field_labels:
            if field.name == f'{self.model.objects.model._meta.db_table}_id':
                pass
            elif field.name in model_label:
                pass
            # elif not field.editable:
            #     pass
            else:
                field_label.append(field.name)
        return field_label

    def get_template_name_label(self):
        if self.template_label == '0':
            template_name = f'{self.app_label}/{self.model_label}_create.html'
        elif self.template_label:
           path = self.template_label.split("-")
           file = ""
           for folder in path:
                file += folder + "/"
           template_name = f'{file[:-1]}.html'
        else:
            template_name = 'modelobject_list.html'
        return template_name

    def get_permissions_required_label(self, permission=None, permission_type=None):
        if permission is not None:
            permission_required_label = permission
        else:
            if permission_type is None:
                permission_required_label = (f'{self.app_label}.view_{self.model_label}',
                                             f'{self.app_label}.add_{self.model_label}',
                                             f'{self.app_label}.change_{self.model_label}',
                                             f'{self.app_label}.delete_{self.model_label}')
            elif permission_type == "view":
                permission_required_label = f'{self.app_label}.view_{self.model_label}'
            elif permission_type == "add":
                permission_required_label = f'{self.app_label}.add_{self.model_label}'
            elif permission_type == "change":
                permission_required_label = f'{self.app_label}.change_{self.model_label}'
            elif permission_type == "delete":
                permission_required_label = f'{self.app_label}.delete_{self.model_label}'
            else:
                return HttpResponse(status=403)
        return permission_required_label


class ModelObjectCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
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
        self.get_modelobject_fields_label()

        self.template_label = kwargs.get('template_label', None)
        self.template_name = self.get_template_name_label()

        self.permission_required = self.get_permissions_required_label()
        try:
            ret = super(ModelObjectCreateView, self).dispatch(request, *args, **kwargs)
        except AttributeError:
            raise Http404
        return ret

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_template_name_label(self):
        if self.template_label == '0':
            template_name = f'{self.app_label}/{self.model_label}_create.html'
        elif self.template_label:
            path = self.template_label.split("-")
            file = ""
            for folder in path:
                file += folder + "/"
            template_name = f'{file[:-1]}.html'
        else:
            template_name = 'modelobject_create.html'
        return template_name

    def get_modelobject_fields_label(self, form1=None):
        if not form1 is None:
            self.form_class = form1
        else:
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
            self.fields = field_label
        return 0

    def get_permissions_required_label(self, permission=None, permission_type=None):
        if permission is not None:
            permission_required_label = permission
        else:
            if permission_type is None:
                permission_required_label = (f'{self.app_label}.view_{self.model_label}',
                                             f'{self.app_label}.add_{self.model_label}',
                                             f'{self.app_label}.change_{self.model_label}',
                                             f'{self.app_label}.delete_{self.model_label}')
            elif permission_type == "view":
                permission_required_label = f'{self.app_label}.view_{self.model_label}'
            elif permission_type == "add":
                permission_required_label = f'{self.app_label}.add_{self.model_label}'
            elif permission_type == "change":
                permission_required_label = f'{self.app_label}.change_{self.model_label}'
            elif permission_type == "delete":
                permission_required_label = f'{self.app_label}.delete_{self.model_label}'
            else:
                return HttpResponse(status=403)
        return permission_required_label


class ModelObjectUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
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
        self.get_modelobject_fields_label()

        self.template_label = kwargs.get('template_label', None)
        self.template_name = self.get_template_name_label()

        self.success_url = self.get_success_url_label()

        self.permission_required = self.get_permissions_required_label()
        try:
            ret = super(ModelObjectUpdateView, self).dispatch(request, *args, **kwargs)
        except AttributeError:
            raise Http404
        return ret

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_template_name_label(self):
        if self.template_label == '0':
            template_name = f'{self.app_label}/{self.model_label}_create.html'
        elif self.template_label:
            path = self.template_label.split("-")
            file = ""
            for folder in path:
                file += folder + "/"
            template_name = f'{file[:-1]}.html'
        else:
            template_name = 'modelobject_create.html'
        return template_name

    def get_modelobject_fields_label(self, form1=None):
        if not form1 is None:
            self.form_class = form1
        else:
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
            self.fields = field_label
        return 0

    def get_success_url_label(self):
        if self.success_label == "0":
            success_url = 'modelobject_success_url.html'
        elif self.success_label == "1":
            success_url = f'{self.app_label}/{self.model_label}_success_url.html'
        elif self.success_label:
            success_url = self.success_label
        else:
            success_url = reverse('MySchoolHome:modelobject_list_view', kwargs={'app_label':self.app_label, 'model_label':self.model_label})
        return success_url

    def get_permissions_required_label(self, permission=None, permission_type=None):
        if permission is not None:
            permission_required_label = permission
        else:
            if permission_type is None:
                permission_required_label = (f'{self.app_label}.view_{self.model_label}',
                                             f'{self.app_label}.add_{self.model_label}',
                                             f'{self.app_label}.change_{self.model_label}',
                                             f'{self.app_label}.delete_{self.model_label}')
            elif permission_type == "view":
                permission_required_label = f'{self.app_label}.view_{self.model_label}'
            elif permission_type == "add":
                permission_required_label = f'{self.app_label}.add_{self.model_label}'
            elif permission_type == "change":
                permission_required_label = f'{self.app_label}.change_{self.model_label}'
            elif permission_type == "delete":
                permission_required_label = f'{self.app_label}.delete_{self.model_label}'
            else:
                return HttpResponse(status=403)
        return permission_required_label


class ModelObjectDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
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

        self.permission_required = self.get_permissions_required_label()
        try:
            ret = super(ModelObjectDeleteView, self).dispatch(request, *args, **kwargs)
        except AttributeError:
            raise Http404
        except TemplateDoesNotExist:
            return HttpResponse(status=501)
        return ret

    def get_template_name_label(self):
        if self.template_label == "0":
            template_name = f'{self.app_label}/{self.model_label}_delete.html'
        elif self.template_label:
            path = self.template_label.split("-")
            file = ""
            for folder in path:
                file += folder + "/"
            template_name = f'{file[:-1]}.html'
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

    def get_permissions_required_label(self, permission=None, permission_type=None):
        if permission is not None:
            permission_required_label = permission
        else:
            if permission_type is None:
                permission_required_label = (f'{self.app_label}.view_{self.model_label}',
                                             f'{self.app_label}.add_{self.model_label}',
                                             f'{self.app_label}.change_{self.model_label}',
                                             f'{self.app_label}.delete_{self.model_label}')
            elif permission_type == "view":
                permission_required_label = f'{self.app_label}.view_{self.model_label}'
            elif permission_type == "add":
                permission_required_label = f'{self.app_label}.add_{self.model_label}'
            elif permission_type == "change":
                permission_required_label = f'{self.app_label}.change_{self.model_label}'
            elif permission_type == "delete":
                permission_required_label = f'{self.app_label}.delete_{self.model_label}'
            else:
                return HttpResponse(status=403)
        return permission_required_label