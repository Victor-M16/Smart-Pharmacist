from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .models import VendingMachine, Dispensation, Inventory, VendingSlot

# Register your models here.

class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'username', )
    list_filter = ('username','email', 'account_type',  'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'username','account_type',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email','phone', 'national_id','account_type', 'entity_id')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Important dates', {'fields': ('start_date',)}),  # Add important dates if needed
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
            ('Agent', 'Agent'),
            ('Citizen', 'Citizen'),
            ('Entity Admin', 'Entity Admin'),
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



admin.site.register(User)
