from django.contrib import admin
from .models import Patient, Doctor, Medication, Prescription, PrescriptionMedication, Pharmacist
from .models import VendingMachine, Dispensation, Inventory, VendingSlot

# Register your models here.

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Medication)
admin.site.register(Prescription)
admin.site.register(PrescriptionMedication)
admin.site.register(VendingMachine)
admin.site.register(Dispensation)
admin.site.register(Inventory)
admin.site.register(VendingSlot)
admin.site.register(Pharmacist)
