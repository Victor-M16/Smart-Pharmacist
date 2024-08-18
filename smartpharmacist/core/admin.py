from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'username', )
    list_filter = ('username','email', 'account_type',  'is_active', 'is_staff')
    ordering = ('-created_at',)
    list_display = ('email', 'username','account_type',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email','phone', 'national_id','account_type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Important dates', {'fields': ('created_at',)}),  # Add important dates if needed
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name','email', 'username','account_type', 'password1', 'password2', 'is_active', 'is_staff', )}
         ),
    )

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'account_type':
            kwargs['choices'] = (
        ('Doctor', 'Doctor'),
        ('Patient', 'Patient'),
        ('Pharmacist', 'Pharmacist'),
        ('Admin', 'Admin'),
            )
        return super().formfield_for_choice_field(db_field, request, **kwargs)
    
admin.site.register(Medication)
admin.site.register(Prescription)
admin.site.register(PrescriptionMedication)
admin.site.register(VendingMachine)
admin.site.register(Dispensation)
admin.site.register(Inventory)
admin.site.register(VendingSlot)

admin.site.register(User, UserAdminConfig)
