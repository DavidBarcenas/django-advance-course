from rest_framework import serializers

from cride.circles.models import Circle


class CircleModelSerializer(serializers.ModelSerializer):

    model = Circle
    fields = (
       'id', 'name', 'slug_name',
       'about', 'picture',
       'rides_offered', 'rides_taken',
       'is_verified', 'is_public',
       'is_limited', 'members_limit' 
    )
