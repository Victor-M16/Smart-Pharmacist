from rest_framework import permissions

class IsAccountType(permissions.BasePermission):
    account_type = None

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.account_type == self.account_type
        )

class IsPatientOnly(IsAccountType):
    account_type = 'Patient'

class IsDoctorOnly(IsAccountType):
    account_type = 'Doctor'

class IsPharmacistOnly(IsAccountType):
    account_type = 'Pharmacist'



class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read-only access for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow update and delete if user is admin or the object owner
        return request.user.is_staff or obj == request.user

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Only allow access if user is an admin
        return request.user and request.user.is_staff