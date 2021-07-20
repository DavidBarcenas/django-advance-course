from cride.circles.models.memberships import Membership
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from cride.circles.models.circles import Circle
from cride.circles.serializers.circles import CircleModelSerializer


class CircleViewSet(viewsets.ModelViewSet):
    
    serializer_class = CircleModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Restrict list to public-only"""

        queryset = Circle.objects.all()

        if self.action == 'list':
            return queryset.filter(is_public=True)

        return queryset

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