from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('login/',views.login, name='login' ),
    path('register/',views.register, name='register' ),
    path('doc-prescription/',views.doc_prescription, name='doc-prescription' ),
    path('new-patient/',views.create_patient, name='new-patient' ),
    path('new-prescription/',views.create_prescription, name='new-prescription' ),
    path('pat-home/',views.patient_home, name='pat-home' ),
    path('pharm-home/',views.pharmacist_home, name='pharm-home' ),
    path('new-medication/',views.create_medication, name='new-medication' ),


]
