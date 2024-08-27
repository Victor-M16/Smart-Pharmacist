from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    #template needs reworking
    path('logout/', auth_views.LogoutView.as_view(template_name='auth/logout.html'), name='logout'),
    path('register/',views.CustomRegisterView.as_view(), name='register' ),

    #authenticated doctor sees prescriptions
    path('doc-prescription/',views.doc_prescription, name='doc-prescription' ),
    path('new-patient/',views.create_patient, name='new-patient' ),
    path('new-prescription/',views.create_prescription, name='new-prescription' ),
    path('new-medication/',views.create_medication, name='new-medication' ),
]
