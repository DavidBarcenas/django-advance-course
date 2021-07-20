from rest_framework.permissions import BasePermission
from cride.circles.models import Membership


class IsCircleAdmin(BasePermission):
    """Allow access only to circle amdins."""

    def has_object_permission(self, request, view, obj):
        """Verify user have a membership in the object."""

        try:
            Membership.objects.get(
                user = request.user,
                circle = obj,
                is_admin = True,
                is_active = True
            )
        except Membership.DoesNotExist:
            return False

        return True

