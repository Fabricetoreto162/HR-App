from django.urls import path
from .views import EmployeeListCreateView, EmployeeDetailView

urlpatterns = [
    path('', EmployeeListCreateView.as_view(), name='employee-list-create'),  # GET / POST
    path('<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),    # GET / DELETE
]