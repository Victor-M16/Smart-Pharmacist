from rest_framework import permissions

# class IsInGroupOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission to only allow members of a specific group to create objects.
#     """

#     def has_permission(self, request, view):
#         # Check if the request method is safe (GET, HEAD, OPTIONS)
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         # Check if the user is authenticated
#         if request.user and request.user.is_authenticated:
#             # Check if the user belongs to a specific group (e.g., pharmacists)
#             # Adjust this logic according to your actual group or role requirements
#             return request.user.groups.filter(name='Doctors').exists()

#         return False


class IsPatientOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_patient

class IsDoctorOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_doctor
    
class IsPharmacistOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_pharmacist

