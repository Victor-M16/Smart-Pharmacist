from django.contrib.auth.models import (AbstractBaseUser, AbstractUser,
                                        BaseUserManager, PermissionsMixin)
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(username, password, **other_fields)

    def create_user(self, username, password=None, **other_fields):
        if not username:
            raise ValueError(_('You must provide a username'))

        user = self.model(username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ACCOUNT_TYPE_CHOICES = (
        ('Doctor', 'Doctor'),
        ('Patient', 'Patient'),
        ('Pharmacist', 'Pharmacist'),
        ('Admin', 'Admin'),
    )

    SPECIALTY_CHOICES = (
        ('General', 'General'),
        ('Cardiology', 'Cardiology'),
        ('Dermatology', 'Dermatology'),
        ('Endocrinology', 'Endocrinology'),
        ('Gastroenterology', 'Gastroenterology'),
        ('General Surgery', 'General Surgery'),
        ('Hematology', 'Hematology'),
        ('Infectious Disease', 'Infectious Disease'),
        ('Nephrology', 'Nephrology'),
        ('Neurology', 'Neurology'),
        ('Obstetrics & Gynecology', 'Obstetrics & Gynecology'),
        ('Oncology', 'Oncology'),
        ('Ophthalmology', 'Ophthalmology'),
        ('Orthopedic Surgery', 'Orthopedic Surgery'),
        ('Otolaryngology', 'Otolaryngology'),
        ('Pediatrics', 'Pediatrics'),
        ('Psychiatry', 'Psychiatry'),
        ('Pulmonology', 'Pulmonology'),
        ('Radiology', 'Radiology'),
        ('Rheumatology', 'Rheumatology'),
        ('Urology', 'Urology'),
    )

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=150, null=True, choices=ACCOUNT_TYPE_CHOICES)
    specialty = models.CharField(max_length=100, null=True, blank=True, choices=SPECIALTY_CHOICES)
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    national_id = models.CharField(max_length=20, null=True, blank=True, unique=True)
    dob = models.DateField(_('dob'), null=True, blank=True)
    gender = models.CharField(max_length=255, null= True)
    id_data = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    # is_patient = models.BooleanField(default=False)
    # is_doctor = models.BooleanField(default=False)
    # is_pharmacist = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        if self.first_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("user-detail", kwargs={"pk": self.pk})



class Medication(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Prescription(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE,related_name = "Patient")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "Doctor")
    code = models.CharField(max_length=4, unique=True, null=True, blank=True) #auto-generated
    sickness = models.CharField(max_length=100) 
    is_dispensed = models.BooleanField(default=False) #flag 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} for {self.patient}"
   
class PrescriptionMedication(models.Model):
    id = models.AutoField(primary_key=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    instructions = models.TextField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.medication} for {self.prescription.code}"
    
class VendingMachine(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.location
    
class VendingSlot(models.Model):
    id = models.AutoField(primary_key=True)
    vending_machine = models.ForeignKey(VendingMachine, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    slot_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vending_machine} - {self.slot_number} - {self.medication}"

class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    vending_machine = models.ForeignKey(VendingMachine, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#deprecate
class Dispensation(models.Model):
    id = models.AutoField(primary_key=True)
    vending_machine = models.ForeignKey(VendingMachine, on_delete=models.CASCADE)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Test(models.Model):
    field1 = models.CharField(max_length=255)
    field2 = models.IntegerField()

    