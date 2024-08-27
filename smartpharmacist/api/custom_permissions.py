from rest_framework import permissions
from rest_framework.response import Response

class IsPatientOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Debugging line
        print("Checking patient user permission")
        return request.user and request.user.is_patient

class IsDoctorOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # Debugging line
        print("Checking doctor user permission")
        return request.user and request.user.is_doctor
    
class IsPharmacistOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Debugging line
        print("Checking pharmacist user permission")
        return request.user and request.user.is_pharmacist

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or obj == request.user

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Debugging line
        print("Checking admin user permission")
        return request.user and request.user.is_staff