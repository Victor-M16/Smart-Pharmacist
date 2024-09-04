# urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import *

app_name = 'api'

router = DefaultRouter()
router.register(r'tests', TestViewSet)
router.register(r'users', UserViewSet, basename='users')
router.register(r'patients', PatientViewSet, basename='patients')
router.register(r'doctors', DoctorViewSet, basename='doctors')
router.register(r'medications', MedicationViewSet, basename='medications')
router.register(r'vending-machines', VendingMachineViewSet, basename='vending-machines')
router.register(r'vending-slots', VendingSlotViewSet, basename='vending-slots')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescriptions')
router.register(r'prescription-medications', PrescriptionMedicationViewSet, basename='prescription-medications')
router.register(r'dispensations', DispensationViewSet, basename='dispensations')

urlpatterns = [
    path('', include(router.urls)),
    path('esp32/', ESP32_API.as_view()),

    #for authentication of the vending machines
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
