from rest_framework.permissions import BasePermission


class IsRideOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        """Verify requesting user is the ride create."""
        return request.user == obj.offered_by

class IsNotRideOwner(BasePermission):
    """Only users that aren't ride owner can call the views"""
    def has_object_permission(self, request, view, obj):
        return not request.user == obj.offered_by