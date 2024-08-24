from rest_framework import serializers
from core.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'account_type', 'specialty', 
            'email', 'phone','national_id', 'dob', 'gender', 
            'id_data', 'created_at', 'updated_at'
        ]

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    patient = UserSerializer()
    doctor = UserSerializer()

    class Meta:
        model = Prescription
        fields = '__all__'

class PrescriptionMedicationSerializer(serializers.ModelSerializer):
    prescription = PrescriptionSerializer()
    medication = MedicationSerializer()

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


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
