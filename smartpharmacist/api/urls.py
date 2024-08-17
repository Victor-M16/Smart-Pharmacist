from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/', UserRetrieveView.as_view(), name='user-retrieve'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', UserDestroyView.as_view(), name='user-delete'),
    
    path('medications/', MedicationListView.as_view(), name='medication-list'),
    path('medications/create/', MedicationCreateView.as_view(), name='medication-create'),
    path('medications/<int:pk>/', MedicationRetrieveView.as_view(), name='medication-retrieve'),
    path('medications/<int:pk>/delete/', MedicationDestroyView.as_view(), name='medication-destroy'),
    path('medications/<int:pk>/update/', MedicationUpdateView.as_view(), name='medication-update'),

    path('vending-machines/', VendingMachineListView.as_view(), name='vendingmachine-list'),
    path('vending-machines/create/', VendingMachineCreateView.as_view(), name='vendingmachine-create'),
    path('vending-machines/<int:pk>/', VendingMachineRetrieveView.as_view(), name='vendingmachine-retrieve'),
    path('vending-machines/<int:pk>/delete/', VendingMachineDestroyView.as_view(), name='vendingmachine-destroy'),
    path('vending-machines/<int:pk>/update/', VendingMachineUpdateView.as_view(), name='vendingmachine-update'),

    path('vending-slots/', VendingSlotListView.as_view(), name='vendingslot-list'),
    path('vending-slots/create/', VendingSlotCreateView.as_view(), name='vendingslot-create'),
    path('vending-slots/<int:pk>/', VendingSlotRetrieveView.as_view(), name='vendingslot-retrieve'),
    path('vending-slots/<int:pk>/delete/', VendingSlotDestroyView.as_view(), name='vendingslot-destroy'),
    path('vending-slots/<int:pk>/update/', VendingSlotUpdateView.as_view(), name='vendingslot'),



    # Prescription URLs
    path('prescriptions/', PrescriptionListView.as_view(), name='prescription-list'),
    path('prescriptions/create/', PrescriptionCreateView.as_view(), name='prescription-create'),
    path('prescriptions/<int:pk>/', PrescriptionRetrieveView.as_view(), name='prescription-retrieve'),
    path('prescriptions/<int:pk>/delete/', PrescriptionDestroyView.as_view(), name='prescription-destroy'),
    path('prescriptions/<int:pk>/update/', PrescriptionUpdateView.as_view(), name='prescription-update'),

    # PrescriptionMedication URLs
    path('prescription-medications/', PrescriptionMedicationListView.as_view(), name='prescriptionmedication-list'),
    path('prescription-medications/create/', PrescriptionMedicationCreateView.as_view(), name='prescriptionmedication-create'),
    path('prescription-medications/<int:pk>/', PrescriptionMedicationRetrieveView.as_view(), name='prescriptionmedication-retrieve'),
    path('prescription-medications/<int:pk>/delete/', PrescriptionMedicationDestroyView.as_view(), name='prescriptionmedication-destroy'),
    path('prescription-medications/<int:pk>/update/', PrescriptionMedicationUpdateView.as_view(), name='prescriptionmedication-update'),


    path('api/test/', test_api, name='test_api'),
]
