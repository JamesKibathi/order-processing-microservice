from django.db import models

from api.utils.helpers import get_uuid



class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class BaseModel(models.Model):
    """
    An abstract base class model that provides self updating
    ``created`` and ``updated`` fields with UUID primary key.
    """
    id = models.UUIDField(primary_key=True, default=get_uuid, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    objects = CustomManager()

    class Meta:
        abstract = True

