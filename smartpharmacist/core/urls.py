from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/',views.create_user, name='register' ),
    path('doc-prescription/',views.doc_prescription, name='doc-prescription' ),
    path('new-patient/',views.create_patient, name='new-patient' ),
    path('new-prescription/',views.create_prescription, name='new-prescription' ),
    path('new-medication/',views.create_medication, name='new-medication' ),
]
