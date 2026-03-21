from rest_framework.permissions import BasePermission


class IsEngineeringOrAdmin(BasePermission):
    """Allow access only to engineering and admin roles."""
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and
                request.user.role in ['engineering', 'admin'])


class IsApproverOrAdmin(BasePermission):
    """Allow access only to approver and admin roles."""
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and
                request.user.role in ['approver', 'admin'])


class IsAdminOnly(BasePermission):
    """Allow access only to admin role."""
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and
                request.user.role == 'admin')
