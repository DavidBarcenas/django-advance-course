from rest_framework import serializers
from cride.users.models.profiles import Profile

class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer"""

   

    class Meta:
        model = Profile
        fields = (
            'picture',
            'biography',
            'rides_taken',
            'rides_offered',
            'reputation'
        )
        read_only_fields = (
            'rides_taken',
            'rides_offered',
            'reputation'
        )
