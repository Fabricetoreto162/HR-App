from django.db import models
from employees.models import Employee

class Attendance(models.Model):
    STATUS_CHOICES = (
    ('present', 'Présent'),
    ('retard', 'Retard'),
    ('absent', 'Absent'),
    ('depart_anticipe', 'Départ anticipé'),)


    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='absent')
    minutes_late = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.full_name} - {self.date}"
