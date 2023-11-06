from django.db import models


class TimeStampAbstractModel(models.Model):
    created_at = models.DateTimeField('дата добавление', auto_now_add=True)
    updated_at = models.DateTimeField('дата изменения', auto_now=True)

    class Meta:
        abstract = True