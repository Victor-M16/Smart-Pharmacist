from rest_framework import generics
from core.models import *
from .serializers import *
from .custom_permissions import *
from rest_framework import permissions
import requests
from django.http import JsonResponse



class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsDoctorOnly] 

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsDoctorOnly, IsAdminUser] 

class UserRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsDoctorOnly, IsOwnerOrAdmin]  

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsDoctorOnly, IsOwnerOrAdmin]  

class UserDestroyView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsDoctorOnly, IsOwnerOrAdmin]  



# Medication views
class MedicationListView(generics.ListAPIView):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [permissions.AllowAny]  

class MedicationCreateView(generics.CreateAPIView):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [IsDoctorOnly]  

class MedicationRetrieveView(generics.RetrieveAPIView):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [permissions.AllowAny]

class MedicationDestroyView(generics.DestroyAPIView):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [IsDoctorOnly]

class MedicationUpdateView(generics.UpdateAPIView):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [IsDoctorOnly]



# Vending Machine views
class VendingMachineListView(generics.ListAPIView):
    queryset = VendingMachine.objects.all()
    serializer_class = VendingMachineSerializer
    permission_classes = [permissions.AllowAny]  

class VendingMachineCreateView(generics.CreateAPIView):
    queryset = VendingMachine.objects.all()
    serializer_class = VendingMachineSerializer
    permission_classes = [IsPharmacistOnly]  


class VendingMachineRetrieveView(generics.RetrieveAPIView):
    queryset = VendingMachine.objects.all()
    serializer_class = VendingMachineSerializer
    permission_classes = [permissions.AllowAny]

class VendingMachineDestroyView(generics.DestroyAPIView):
    queryset = VendingMachine.objects.all()
    serializer_class = VendingMachineSerializer
    permission_classes = [IsPharmacistOnly]

class VendingMachineUpdateView(generics.UpdateAPIView):
    queryset = VendingMachine.objects.all()
    serializer_class = VendingMachineSerializer
    permission_classes = [IsPharmacistOnly]


# Vending Slot views
class VendingSlotListView(generics.ListAPIView):
    queryset = VendingSlot.objects.all()
    serializer_class = VendingSlotSerializer
    permission_classes = [permissions.AllowAny]  

class VendingSlotCreateView(generics.CreateAPIView):
    queryset = VendingSlot.objects.all()
    serializer_class = VendingSlotSerializer
    permission_classes = [IsPharmacistOnly]  

class VendingSlotRetrieveView(generics.RetrieveAPIView):
    queryset = VendingSlot.objects.all()
    serializer_class = VendingSlotSerializer
    permission_classes = [permissions.AllowAny]

class VendingSlotDestroyView(generics.DestroyAPIView):
    queryset = VendingSlot.objects.all()
    serializer_class = VendingSlotSerializer
    permission_classes = [IsPharmacistOnly]

class VendingSlotUpdateView(generics.UpdateAPIView):
    queryset = VendingSlot.objects.all()
    serializer_class = VendingSlotSerializer
    permission_classes = [IsPharmacistOnly]



#prescription views
class PrescriptionListView(generics.ListAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.AllowAny]

class PrescriptionCreateView(generics.CreateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsPharmacistOnly]

class PrescriptionRetrieveView(generics.RetrieveAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.AllowAny]

class PrescriptionDestroyView(generics.DestroyAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsPharmacistOnly]

class PrescriptionUpdateView(generics.UpdateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsPharmacistOnly]



#prescriptionmedication views
class PrescriptionMedicationListView(generics.ListAPIView):
    serializer_class = PrescriptionMedicationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = PrescriptionMedication.objects.all()
        prescription_id = self.request.query_params.get('prescription')
        
        if prescription_id:
            queryset = queryset.filter(prescription_id=prescription_id)
        
        return queryset

class PrescriptionMedicationCreateView(generics.CreateAPIView):
    queryset = PrescriptionMedication.objects.all()
    serializer_class = PrescriptionMedicationSerializer
    permission_classes = [IsPharmacistOnly]

class PrescriptionMedicationRetrieveView(generics.RetrieveAPIView):
    queryset = PrescriptionMedication.objects.all()
    serializer_class = PrescriptionMedicationSerializer
    permission_classes = [permissions.AllowAny]

class PrescriptionMedicationDestroyView(generics.DestroyAPIView):
    queryset = PrescriptionMedication.objects.all()
    serializer_class = PrescriptionMedicationSerializer
    permission_classes = [IsPharmacistOnly]

class PrescriptionMedicationUpdateView(generics.UpdateAPIView):
    queryset = PrescriptionMedication.objects.all()
    serializer_class = PrescriptionMedicationSerializer
    permission_classes = [IsPharmacistOnly]






ESP32_IP = "192.168.8.124"  
def test_link():
    url = f"http://{ESP32_IP}:80/status" 
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("Successfully linked ESP32")
            return data["status"]
        else:
            print("Failed to get status")
            return None
    except:
        pass


def test_api(request):
    if request.method == 'GET':
        test_link()
        return JsonResponse({'message': 'Request received from ESP32'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)