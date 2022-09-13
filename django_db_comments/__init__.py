import django

__version__ = "0.4.1"

if django.VERSION < (3, 2):
    default_app_config = "django_db_comments.apps.DjangoDbCommentsConfig"
