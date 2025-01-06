# flake8: noqa

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dj_waanverse_auth"
    label = "dj_waanverse_auth"
    verbose_name = "Waanverse Auth"
