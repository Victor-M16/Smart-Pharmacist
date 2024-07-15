from django.urls import path
from . import views  

urlpatterns = [
    path('doctors/', views.DoctorListView.as_view(), name='doctor-list'),
    path('doctors/create/', views.DoctorCreateView.as_view(), name='doctor-create'),

    path('patients/', views.PatientListView.as_view(), name='patient-list'),
    path('patients/create/', views.PatientCreateView.as_view(), name='patient-create'),

    path('medications/', views.MedicationListView.as_view(), name='medication-list'),
    path('medications/create/', views.MedicationCreateView.as_view(), name='medication-create'),

    path('vendingmachines/', views.VendingMachineListView.as_view(), name='vendingmachine-list'),
    path('vendingmachines/create/', views.VendingMachineCreateView.as_view(), name='vendingmachine-create'),

    path('vendingslots/', views.VendingSlotListView.as_view(), name='vendingslot-list'),
    path('vendingslots/create/', views.VendingSlotCreateView.as_view(), name='vendingslot-create'),
]
