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

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'phone','created_at', 'updated_at']

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    formatted_created_at = serializers.SerializerMethodField()
    formatted_updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'doctor', 'code', 'sickness', 'is_dispensed', 'formatted_created_at', 'formatted_updated_at']

    def get_formatted_created_at(self, obj):
        return obj.created_at.strftime("%B %d, %Y, %I:%M %p")

    def get_formatted_updated_at(self, obj):
        return obj.updated_at.strftime("%B %d, %Y, %I:%M %p")

class PrescriptionMedicationSerializer(serializers.ModelSerializer):
    formatted_created_at = serializers.SerializerMethodField()
    formatted_updated_at = serializers.SerializerMethodField()

    class Meta:
        model = PrescriptionMedication
        fields = ['id', 'prescription', 'medication', 'instructions', 'formatted_created_at', 'formatted_updated_at']

    def get_formatted_created_at(self, obj):
        return obj.created_at.strftime("%B %d, %Y, %I:%M %p")

    def get_formatted_updated_at(self, obj):
        return obj.updated_at.strftime("%B %d, %Y, %I:%M %p")

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
