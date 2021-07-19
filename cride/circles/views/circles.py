from rest_framework import viewsets

from cride.circles.models.circles import Circle
from cride.circles.serializers.circles import CircleModelSerializer


class CircleViewSet(viewsets.ModelViewSet):
    
    queryset = Circle.objects.all()
    serializer_class = CircleModelSerializer