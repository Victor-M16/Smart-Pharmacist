from rest_framework import serializers
from core.models import Patient, Doctor, Pharmacist, Medication, Prescription, PrescriptionMedication, VendingMachine, Dispensation, Inventory, VendingSlot


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
 
class PharmacistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacist
        fields = '__all__'

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ('id', 'name','description','package_size','created_at','updated_at')

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

class PrescriptionMedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionMedication
        fields = '__all__'

class VendingMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendingMachine
        fields = '__all__'

class DispensationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispensation
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

class VendingSlotSerializer(serializers.ModelSerializer):
    medication = MedicationSerializer() 

    class Meta:
        model = VendingSlot
        fields = ('id', 'vending_machine', 'medication', 'slot_number', 'created_at', 'updated_at')
