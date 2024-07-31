from django.urls import path
from .views import (
    DoctorListView, DoctorCreateView, DoctorRetrieveView, DoctorDestroyView, DoctorUpdateView,
    PatientListView, PatientCreateView, PatientRetrieveView, PatientDestroyView, PatientUpdateView,
    MedicationListView, MedicationCreateView, MedicationRetrieveView, MedicationDestroyView, MedicationUpdateView,
    VendingMachineListView, VendingMachineCreateView, VendingMachineRetrieveView, VendingMachineDestroyView, VendingMachineUpdateView,
    VendingSlotListView, VendingSlotCreateView, VendingSlotRetrieveView, VendingSlotDestroyView, VendingSlotUpdateView, test_api
)

urlpatterns = [
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/create/', DoctorCreateView.as_view(), name='doctor-create'),
    path('doctors/<int:pk>/', DoctorRetrieveView.as_view(), name='doctor-retrieve'),
    path('doctors/<int:pk>/delete/', DoctorDestroyView.as_view(), name='doctor-destroy'),
    path('doctors/<int:pk>/update/', DoctorUpdateView.as_view(), name='doctor-update'),

    path('patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/create/', PatientCreateView.as_view(), name='patient-create'),
    path('patients/<int:pk>/', PatientRetrieveView.as_view(), name='patient-retrieve'),
    path('patients/<int:pk>/delete/', PatientDestroyView.as_view(), name='patient-destroy'),
    path('patients/<int:pk>/update/', PatientUpdateView.as_view(), name='patient-update'),

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


    path('api/test/', test_api, name='test_api'),
]
