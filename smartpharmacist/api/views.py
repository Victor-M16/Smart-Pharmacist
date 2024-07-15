from rest_framework import generics
from core.models import Patient, Doctor, Medication, Prescription, PrescriptionMedication, VendingMachine, Dispensation, Inventory, VendingSlot
from .serializers import PatientSerializer, DoctorSerializer, MedicationSerializer, PrescriptionSerializer, PrescriptionMedicationSerializer, VendingMachineSerializer, DispensationSerializer, InventorySerializer, VendingSlotSerializer
from .custom_permissions import IsInGroupOrReadOnly, IsDoctorOnly, IsPatientOnly, IsPharmacistOnly
from rest_framework import permissions

# Doctor views
class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsDoctorOnly]

class DoctorCreateView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsDoctorOnly]

# Patient views
class PatientListView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsPatientOnly]

class PatientCreateView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsDoctorOnly]  # Adjust as per your application logic

# Medication views
class MedicationListView(generics.ListAPIView):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [permissions.AllowAny]  # Example permission, adjust as needed

class MedicationCreateView(generics.CreateAPIView):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [IsDoctorOnly]  # Adjust as per your application logic

# Vending Machine views
class VendingMachineListView(generics.ListAPIView):
    queryset = VendingMachine.objects.all()
    serializer_class = VendingMachineSerializer
    permission_classes = [permissions.AllowAny]  # Example permission, adjust as needed

class VendingMachineCreateView(generics.CreateAPIView):
    queryset = VendingMachine.objects.all()
    serializer_class = VendingMachineSerializer
    permission_classes = [IsPharmacistOnly]  # Adjust as per your application logic

# Vending Slot views
class VendingSlotListView(generics.ListAPIView):
    queryset = VendingSlot.objects.all()
    serializer_class = VendingSlotSerializer
    permission_classes = [permissions.AllowAny]  # Example permission, adjust as needed

class VendingSlotCreateView(generics.CreateAPIView):
    queryset = VendingSlot.objects.all()
    serializer_class = VendingSlotSerializer
    permission_classes = [IsPharmacistOnly]  # Adjust as per your application logic
