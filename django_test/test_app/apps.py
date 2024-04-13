from django.apps import AppConfig


class TestAppConfig(AppConfig):
    verbose_name = "Известные женщины мира"
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_app'
