from rest_framework import generics
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # Optionnel : redéfinir create pour forcer la génération QR si besoin
    def perform_create(self, serializer):
        employee = serializer.save()
        # Le QR code est déjà généré dans le save() du modèle
        return employee


class EmployeeDetailView(generics.RetrieveDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer