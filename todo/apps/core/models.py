import uuid
from django.db import models


class BaseModel(models.Model):
    """
    Base model for all models

    Attributes:
        id: Auto-incrementing primary key
        uid: UUID field
        created_at: DateTime field for creation timestamp
        updated_at: DateTime field for last update timestamp
        is_active: Boolean field to track active status
    """
    id = models.AutoField(primary_key=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
