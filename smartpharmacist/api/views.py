
import os
import random

import requests
from core.models import *
from django.conf import settings
from django.http import JsonResponse
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from twilio.rest import Client
from .custom_permissions import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response


# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    
class PatientViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(account_type="Patient")
    serializer_class = PatientSerializer
    permission_classes = [IsAdminUser | IsPharmacistOnly | IsDoctorOnly]

    def perform_create(self, serializer):
        serializer.save(account_type="Patient", is_patient=True)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(account_type="Doctor")
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

# Medication ViewSet
class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [IsAdminUser | IsPharmacistOnly | IsDoctorOnly]

# Vending Machine ViewSet
class VendingMachineViewSet(viewsets.ModelViewSet):
    queryset = VendingMachine.objects.all()
    serializer_class = VendingMachineSerializer
    permission_classes = [IsAdminUser | IsPharmacistOnly]

# Vending Slot ViewSet
class VendingSlotViewSet(viewsets.ModelViewSet):
    queryset = VendingSlot.objects.all()
    serializer_class = VendingSlotSerializer
    permission_classes = [IsAdminUser | IsPharmacistOnly | IsDoctorOnly]

class PrescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAdminUser | IsPharmacistOnly | IsDoctorOnly]

    def get_queryset(self):
        user = self.request.user
        return Prescription.objects.filter(doctor=user.id)

    def perform_create(self, serializer):
        # Generate a unique 4-digit code
        code = self.generate_unique_code()
        # Save the prescription with the generated code
        # prescription = serializer.save(code=code)
        serializer.save(code=code)
        print("Prescription created, waiting for medications to be added")

    @action(detail=True, methods=['post'])
    def send_sms(self, request, pk=None):
        try:
            prescription = self.get_object()
            self.send_patient_sms(prescription)
            return Response({"status": "success"}, status=200)
        except Prescription.DoesNotExist:
            return Response({"status": "error", "message": "Prescription not found"}, status=404)

    def send_patient_sms(self, prescription):
        account_sid = settings.TWILIO_SID
        auth_token = settings.TWILIO_TOKEN
        twilio_number = '+13183247275'

        client = Client(account_sid, auth_token)

        # Get the patient's phone number from the prescription-patient relationship
        patient_phone = prescription.patient.phone
        prescription_code = prescription.code

        # Fetch the medications and their instructions
        prescribed_meds = PrescriptionMedication.objects.filter(prescription=prescription)
        med_messages = []

        for p in prescribed_meds:
            med = p.medication
            instruction = p.instructions
            med_message = f"{med} - {instruction}"
            med_messages.append(med_message)  # Append to the list of messages

        # Format the SMS message
        meds_list = "\n".join(med_messages)  # Join all medication messages with a newline separator
        sms_message = f'Vending code: {prescription_code}\nMedications:\n{meds_list}' 

        if patient_phone and prescription_code:
            message = client.messages.create(
                from_=twilio_number,
                body=sms_message,
                to=patient_phone
            )

            print(f"Message sent successfully: {message.sid}")
            print(sms_message)
        else:
            print("Patient's phone number or prescription code is not available")

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
    permission_classes = [IsAdminUser | IsPharmacistOnly | IsDoctorOnly]

    def get_queryset(self):
        user = self.request.user
        return PrescriptionMedication.objects.filter(prescription__doctor=user.id)


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