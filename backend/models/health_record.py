from .base import TimeStampedModel
from django.db import models

class HealthRecord(TimeStampedModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='health_records')
    record_type = models.CharField(max_length=50)
    data = models.JSONField()
    source = models.CharField(max_length=100)
    is_synced_with_abha = models.BooleanField(default=False)