from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from cride.circles.models.circles import Circle


class CircleSerializer(serializers.Serializer):
    """Serializer to get the circles."""

    name          = serializers.CharField()
    slug_name     = serializers.SlugField()
    rides_taken   = serializers.IntegerField()
    rides_offered = serializers.IntegerField()
    members_limit = serializers.IntegerField()


class CreateCircleSerializer(serializers.Serializer):
    """Serializer to instantiate circle."""

    name = serializers.CharField(max_length=140)

    slug_name = serializers.SlugField(
        max_length = 40,
        validators = [
            UniqueValidator(queryset=Circle.objects.all())
        ]
    )

    about = serializers.SlugField(
        max_length = 255, 
        required = False
    )

    def create(self, data):
        """Returns a new circle instance."""
        return Circle.objects.create(**data)