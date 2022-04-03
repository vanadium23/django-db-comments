from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField("model creation time")

    class Meta:
        abstract = True


class ExampleModel(TimestampedModel):
    class Meta:
        verbose_name = "This is an example for table comment"


class ProxyModel(ExampleModel):
    class Meta:
        proxy = True


class UnmanagedModel(models.Model):
    class Meta:
        managed = False
