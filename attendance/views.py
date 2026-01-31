from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime, time, timedelta

from .models import Attendance
from .serializers import AttendanceSerializer
from employees.models import Employee

class CheckInView(APIView):
    def post(self, request):
        biometric_id = request.data.get("biometric_id")

        try:
            employee = Employee.objects.get(
                biometric_id=biometric_id,
                is_active=True
            )
        except Employee.DoesNotExist:
            return Response({"error": "Empreinte non reconnue"}, status=404)

        now = timezone.localtime()
        today = now.date()
        current_time = now.time()

        attendance, _ = Attendance.objects.get_or_create(
            employee=employee,
            date=today
        )

        attendance.check_in = current_time
        work_start = employee.work_start_time

        if current_time <= work_start:
            attendance.status = "present"
            attendance.minutes_late = 0
        else:
            diff = (
                timezone.datetime.combine(today, current_time) -
                timezone.datetime.combine(today, work_start)
            )
            attendance.minutes_late = int(diff.total_seconds() // 60)
            attendance.status = "retard"

        attendance.save()
        return Response(AttendanceSerializer(attendance).data, status=200)


class CheckOutView(APIView):
    def post(self, request):
        employee_id = request.data.get('employee_id')

        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=404)

        today = timezone.localdate()

        try:
            attendance = Attendance.objects.get(employee=employee, date=today)
        except Attendance.DoesNotExist:
            return Response({"error": "Attendance not found"}, status=404)

        current_time = timezone.localtime().time()
        attendance.check_out = current_time

        # Heure de sortie selon le poste
        work_end = employee.work_end_time
        if current_time < work_end:
            attendance.status = 'depart_anticipe'  # départ anticipé

        attendance.save()

        return Response(AttendanceSerializer(attendance).data, status=status.HTTP_200_OK)