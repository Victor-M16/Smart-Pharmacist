
import requests, random
from core.models import *
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .custom_permissions import *
from .custom_permissions import (IsAdminUser, IsDoctorOnly, IsOwnerOrAdmin,
                                 IsPharmacistOnly)
from .serializers import *
from .serializers import (MedicationSerializer,
                          PrescriptionMedicationSerializer,
                          PrescriptionSerializer, UserSerializer,
                          VendingMachineSerializer, VendingSlotSerializer, TestSerializer)


# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsDoctorOnly(), IsAdminUser()]
        if self.action in ['create']:
            return [IsDoctorOnly(), IsAdminUser()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsDoctorOnly(), IsAdminUser()]
        return super().get_permissions()
    
class PatientViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(account_type="Patient")
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsDoctorOnly(), IsAdminUser()]
        if self.action in ['create']:
            return [IsDoctorOnly(), IsAdminUser()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsDoctorOnly(), IsAdminUser()]
        return super().get_permissions()
    

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(account_type="Doctor")
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsDoctorOnly(), IsAdminUser()]
        if self.action in ['create']:
            return [IsDoctorOnly(), IsAdminUser()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsDoctorOnly(), IsAdminUser()]
        return super().get_permissions()

# Medication ViewSet
class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsPharmacistOnly(), IsAdminUser()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)

# Vending Machine ViewSet
class VendingMachineViewSet(viewsets.ModelViewSet):
    queryset = VendingMachine.objects.all()
    serializer_class = VendingMachineSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsPharmacistOnly(), IsAdminUser()]
        return super().get_permissions()

# Vending Slot ViewSet
class VendingSlotViewSet(viewsets.ModelViewSet):
    queryset = VendingSlot.objects.all()
    serializer_class = VendingSlotSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsPharmacistOnly(), IsAdminUser()]
        return super().get_permissions()

# Prescription ViewSet
class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsDoctorOnly(), IsAdminUser()]
        return super().get_permissions()

    def perform_create(self, serializer):
        # Generate a unique 4-digit code
        code = self.generate_unique_code()
        # Save the prescription with the generated code
        serializer.save(code=code)

    def generate_unique_code(self):
        # Loop until a unique code is found
        while True:
            # Generate a random 4-digit code
            code = '{:04d}'.format(random.randint(0, 9999))
            # Check if the code already exists
            if not Prescription.objects.filter(code=code).exists():
                return code  


# Prescription Medication ViewSet
class PrescriptionMedicationViewSet(viewsets.ModelViewSet):
    serializer_class = PrescriptionMedicationSerializer

    def get_queryset(self):
        queryset = PrescriptionMedication.objects.all()
        prescription_id = self.request.query_params.get('prescription')
        if prescription_id:
            queryset = queryset.filter(prescription_id=prescription_id)
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsDoctorOnly(), IsAdminUser()]
        return super().get_permissions()
    


class ESP32_API(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ESP32_IP = "192.168.8.124" 

    def test_api(self,request):
        if request.method == 'GET':
            status = self.test_link()
            if status is not None:
                return JsonResponse({'message': 'Request received from ESP32', 'status': status})
            else:
                return JsonResponse({'message': 'Failed to get status from ESP32'}, status=500)
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)

    def test_link(self):
        url = f"http://{self.ESP32_IP}:80/status"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print("Successfully linked ESP32")
                return data.get("status")  # Using .get() to avoid KeyError
            else:
                print("Failed to get status")
                return None
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        

class TestViewSet(viewsets.ModelViewSet):
    serializer_class = TestSerializer
    queryset = Test.objects.all()