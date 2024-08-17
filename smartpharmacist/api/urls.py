# urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (MedicationViewSet, PrescriptionMedicationViewSet,
                    PrescriptionViewSet, UserViewSet, VendingMachineViewSet,
                    VendingSlotViewSet, ESP32_API)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'medications', MedicationViewSet)
router.register(r'vending-machines', VendingMachineViewSet)
router.register(r'vending-slots', VendingSlotViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'prescription-nmedications', PrescriptionMedicationViewSet, basename='prescriptionmedication')


urlpatterns = [
    path('', include(router.urls)),
    path('ESP32/', ESP32_API.as_view()),
]
