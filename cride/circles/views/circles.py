from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from cride.circles.models.circles import Circle
from cride.circles.models.memberships import Membership
from cride.circles.permissions.circles import IsCircleAdmin
from cride.circles.serializers.circles import CircleModelSerializer


class CircleViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    
    serializer_class = CircleModelSerializer
    lookup_field = 'slug_name'

    # filters
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('slug_name', 'name')
    ordering_fields = ('rides_offered', 'rides_taken', 'name', 'created', 'member_limit')
    ordering = ( '-rides_offered', '-rides_taken')
    filter_fields = ('is_verified', 'is_limited')

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