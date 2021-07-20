from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed

from cride.circles.permissions.circles import IsCircleAdmin
from cride.circles.models.circles import Circle
from cride.circles.serializers.circles import CircleModelSerializer
from cride.circles.models.memberships import Membership


class CircleViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    
    serializer_class = CircleModelSerializer

    def get_queryset(self):
        """Restrict list to public-only"""

        queryset = Circle.objects.all()

        if self.action == 'list':
            return queryset.filter(is_public=True)

        return queryset

    def get_permissions(self):
        """Assign permissions based on actions."""
        
        permissions = [IsAuthenticated]

        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)
        
        return [p() for p in permissions]

    def perform_create(self, serializer):
        """Assign circle admin."""

        user    = self.request.user
        circle  = serializer.save()
        profile = user.profile

        Membership.objects.create(
            user     = user,
            profile  = profile,
            circle   = circle,
            is_admin = True,
            remaining_invitations = 10
        )

    def destroy(self, request, pk=None):
        raise MethodNotAllowed('DELETE')