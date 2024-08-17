from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/',views.CustomRegisterView.as_view(), name='register' ),

    #authenticated doctor sees prescriptions
    path('doc-prescription/',views.doc_prescription, name='doc-prescription' ),
    path('new-prescription/',views.create_prescription, name='new-prescription' ),

    #authenticated doctor creates patient
    path('new-patient/',views.create_patient, name='new-patient' ),

    #authenticated pharmacist creates medication
    path('new-medication/',views.create_medication, name='new-medication' ),
]
