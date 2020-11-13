from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

def register_app_db_models_to_django_admin_site(application_name):
    """
    Registers the model(s) defined in the django application with the given django.contrib.admin.site.

    The model(s) in the application should be Model classes, not instances.

    If a model is already registered, raise AlreadyRegistered.

        Args:
            application_name (str): Name of the application in application config.

        Returns:
            bool: The return value. True for success, False otherwise.

        """

    app_models = apps.get_app_config(application_name).get_models()
    for model in app_models:
        try:
            admin.site.register(model)
        except AlreadyRegistered:
            pass
