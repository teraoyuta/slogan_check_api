from django.db import models
from django.utils import timezone


class BaseQuerySet(models.query.QuerySet):
    def delete(self):
        return super(BaseQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(BaseQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class BaseManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(BaseManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return BaseQuerySet(self.model).filter(deleted_at=None)
        return BaseQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()
