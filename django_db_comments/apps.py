# -*- coding: utf-8
from django.apps import AppConfig

from django.db.models.signals import post_migrate

from .db_comments import copy_help_texts_to_database


class DjangoDbCommentsConfig(AppConfig):
    name = "django_db_comments"

    def ready(self):
        post_migrate.connect(copy_help_texts_to_database)
