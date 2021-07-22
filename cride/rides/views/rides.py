from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from cride.circles.models import Circle
from cride.circles.permissions import IsActiveCircleMember
from cride.rides.serializers import CreateRideSerializer


class RideViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):

    serializer_class = CreateRideSerializer
    permission_classes = [IsAuthenticated, IsActiveCircleMember]

    def dispatch(self, request, *args, **kwargs):
        """Verify that the circle exists."""

        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)

        return super(RideViewSet, self).dispatch(request, *args, **kwargs)