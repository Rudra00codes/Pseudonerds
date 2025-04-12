from .base import TimeStampedModel
from django.db import models

class Diagnosis(TimeStampedModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='diagnoses')
    symptoms = models.JSONField()
    diagnosis_result = models.JSONField()
    confidence_score = models.FloatField()
    language = models.CharField(max_length=10, default='en')
    is_reviewed = models.BooleanField(default=False)
    severity_level = models.CharField(
        max_length=20,
        choices=[
            ('LOW', 'Low Risk'),
            ('MEDIUM', 'Medium Risk'),
            ('HIGH', 'High Risk')
        ]
    )