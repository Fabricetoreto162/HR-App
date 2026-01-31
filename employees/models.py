from django.db import models
from datetime import time

class Employee(models.Model):
    full_name = models.CharField(max_length=150)

    position = models.CharField(max_length=100)

    work_start_time = models.TimeField()
    work_end_time = models.TimeField()

    biometric_id = models.CharField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name