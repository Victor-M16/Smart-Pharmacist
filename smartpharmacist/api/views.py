
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
from itertools import cycle
from typing import Dict, Set

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

        if user.account_type == "Doctor":
            return Prescription.objects.filter(doctor=user.id).order_by('created_at')
        else:
            return Prescription.objects.all().order_by('created_at')
        
    def perform_create(self, serializer):
        # Generate a unique 4-digit code
        code = self.generate_unique_code()
        # Save the prescription with the generated code
        # prescription = serializer.save(code=code)
        serializer.save(code=code)
        print("Prescription created, waiting for medications to be added")

    def check_inventory(self, prescription):
        """
        Identifies if any vending machine has all the required prescribed medications with sufficient quantity.
        If found, assigns the vending machine; otherwise, flags it as 'out of stock'.
        """

        # Get all the medications for the given prescription
        prescribed_meds = PrescriptionMedication.objects.filter(prescription=prescription)
        
        # Track machines that have all required medications and their availability status
        potential_machines: Dict[VendingMachine, Set[Medication]] = {}

        # Loop through each prescribed medication
        for prescribed_med in prescribed_meds:
            medication = prescribed_med.medication
            
            # Find all vending slots that contain the required medication
            slots_with_medication = VendingSlot.objects.filter(medication=medication)
            
            # If no vending slots contain this medication, return 'out of stock'
            if not slots_with_medication:
                return "Out of stock"
            
            # Check the inventory for each slot (machine) to see if it has enough medication
            for slot in slots_with_medication:
                inventory = Inventory.objects.filter(vending_machine=slot.vending_machine, medication=medication).first()
                
                # If the inventory for this slot is insufficient, skip this machine
                if inventory and inventory.quantity > 0:
                    # Record or update the machine in the potential machines dictionary
                    if slot.vending_machine not in potential_machines:
                        potential_machines[slot.vending_machine] = {medication: inventory.quantity}
                    else:
                        potential_machines[slot.vending_machine][medication] = inventory.quantity
                else:
                    # If there’s no inventory or insufficient quantity, mark the machine as not suitable for this medication
                    if slot.vending_machine in potential_machines and medication in potential_machines[slot.vending_machine]:
                        del potential_machines[slot.vending_machine][medication]

        # Now we filter out machines that don't contain all medications
        for machine, meds in potential_machines.items():
            # Check if this machine has all the medications in the prescription
            if len(meds) == len(prescribed_meds):
                # All medications are available in sufficient quantities in this machine
                return machine

        # If no vending machine has all the required medications, return 'out of stock'
        return "Out of stock"

    def update_inventory(self, vending_machine, prescribed_meds):

        # inventories = Inventory.objects.filter(vending_machine=vending_machine)
        # med_messages = []
        # for p in prescribed_meds:
        #     med = p.medication
        #     instruction = p.instructions
        #     med_message = f"{med} - {instruction}"
        #     med_messages.append(med_message)  # Append to the list of messages

        pass

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

        # Use check_inventory to find an appropriate vending machine
        vending_machine = self.check_inventory(prescription)

        # Format the SMS message
        meds_list = "\n".join(med_messages)  # Join all medication messages with a newline separator
        
        if vending_machine != "Out of stock":
            # If a vending machine was found, include the location in the SMS
            sms_message = (
                f'Vending code: {prescription_code}\n'
                f'Medications:\n{meds_list}\n'
                f'Machine: {vending_machine.location}.'
            )

            # self.update_inventory(vending_machine,prescribed_meds)
        else:
            # If no vending machine was found, indicate that medications are out of stock
            sms_message = (
                f'Vending code: {prescription_code}\n'
                f'Medications:\n{meds_list}\n'
                f'Mankhwala palibe. Out of stock'
            )

        if patient_phone and prescription_code:
            message = client.messages.create(
                from_=twilio_number,
                body=sms_message,
                to=patient_phone
            )

            # print(f"Message sent successfully: {message.sid}")
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


class DispensationViewSet(viewsets.ModelViewSet):
    queryset = Dispensation.objects.all()
    serializer_class = DispensationSerializer
    permission_classes = [IsAdminUser | IsPharmacistOnly]




# Prescription Medication ViewSet
class PrescriptionMedicationViewSet(viewsets.ModelViewSet):
    serializer_class = PrescriptionMedicationSerializer
    permission_classes = [IsAdminUser | IsPharmacistOnly | IsDoctorOnly]

    def get_queryset(self):
        user = self.request.user
        return PrescriptionMedication.objects.filter(prescription__doctor=user.id).order_by('updated_at')


class ESP32_API(APIView):
    # permission_classes = [IsAdminUser | IsPharmacistOnly]


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
            pass

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
        

    def post(self, request):
        code = request.data.get('code')
        current_slot = int(request.data.get('current_slot', 1))  # Get current slot from ESP32, default to 1 if not provided
        vending_machine_id = request.data.get('vending_machine_id')

        if not code:
            return JsonResponse({'error': 'No code provided'}, status=400)


        try:
            print(f"Received code: {code}, current slot: {current_slot}")
            
            # Fetch the prescription using the provided code
            prescription = Prescription.objects.get(code=code, is_dispensed=False)

            # Fetch the vending machine that made the request
            vending_machine = VendingMachine.objects.get(id=vending_machine_id)

            # Retrieve associated medications and their vending slots
            medications = PrescriptionMedication.objects.filter(prescription=prescription)
            slot_data = []

            # Generate a list of slots for the ESP32 to rotate to
            for med in medications:
                slots = VendingSlot.objects.filter(vending_machine=vending_machine, medication=med.medication)
                slot_data.extend([slot.slot_number for slot in slots])

            # Sort the slots in an optimized order to minimize motor movement
            def get_shortest_path(current, target, total_slots):
                clockwise = (target - current + total_slots) % total_slots
                anticlockwise = (current - target + total_slots) % total_slots
                return min(clockwise, anticlockwise)

            total_slots = 6  # Assuming 6 slots in the vending machine
            sorted_slots = []
            available_slots = slot_data[:]
            while available_slots:
                next_slot = min(available_slots, key=lambda s: get_shortest_path(current_slot, s, total_slots))#from available_slots, for each slot s, get the shortest path from the current slot to s. From those shortest paths, get the smallest one and that slot is selected as the next slot in the optimzed order
                sorted_slots.append(next_slot)
                available_slots.remove(next_slot)
                current_slot = next_slot  # Update current slot to next slot for subsequent movements

    
            # Create the JSON response
            response_data = {
                'prescription_code': prescription.code,
                'vending_slots': sorted_slots  # Send the sorted slots to the ESP32
            }

            prescription.is_dispensed = True
            prescription.save()
            
            # Create a dispensation object to log the dispensation event and which machine dispensed the medication
            self.create_dispensation(vending_machine, prescription)

            return JsonResponse(response_data, status=200)

        except Prescription.DoesNotExist:
            return JsonResponse({'error': 'Prescription not found or already dispensed'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def create_dispensation(self, vending_machine, prescription ):
        """Log the dispensation event"""
        Dispensation.objects.create(vending_machine=vending_machine,prescription=prescription)
        pass



class TestViewSet(viewsets.ModelViewSet):
    serializer_class = TestSerializer
    queryset = Test.objects.all()