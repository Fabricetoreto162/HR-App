from rest_framework import serializers
from .models import Attendance
from datetime import timedelta

class AttendanceSerializer(serializers.ModelSerializer):
    late_duration = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Attendance
        fields = [
            "id",
            "employee",
            "date",
            "check_in",
            "check_out",
            "status",
            "minutes_late",
            "late_duration",
            "created_at",
        ]

    def get_late_duration(self, obj):
        seconds = obj.minutes_late * 60
        return str(timedelta(seconds=seconds))
