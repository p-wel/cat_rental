"""
Setup of apps used
"""
from django.apps import AppConfig


class CatsConfig(AppConfig):
    """Configure Cats app"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "cats"
