from django.shortcuts import render

# Create your views here.

# def home(request):
#     return render(request, "index.html")

def home(request):
    return render(request, "core/doc-home.html", {'title': 'home'})

def login(request):
    return render(request, "auth/login.html", {'title': 'login'})

def register(request):
    return render(request, "auth/register.html", {'title': 'register'})

def doc_prescription(request):
    return render(request, "core/doc-presc.html", {'title': 'prescriptions'})

def create_patient(request):
    return render(request, "core/new-patient.html", {'title': 'new patient'})

def create_prescription(request):
    return render(request, "core/new-prescription.html", {'title': 'new prescription'})

def patient_home(request):
    return render(request, "core/pat-home.html", {'title': 'home'})

def pharmacist_home(request):
    return render(request, "core/pharm-home.html", {'title': 'home'})

def create_medication(request):
    return render(request, "core/new-medication.html", {'title': 'new medication'})

