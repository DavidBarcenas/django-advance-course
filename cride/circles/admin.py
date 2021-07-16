from django.contrib import admin
from cride.circles.models.circles import Circle

@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    """Circle model admin"""

    list_display = (
        'slug_name',
        'name',
        'is_public',
        'is_verified',
        'is_limited',
        'members_limit',
    )

    search_fields = ('slug_name', 'name')

    list_filter = (
        'is_public',
        'is_verified',
        'is_limited',
    )
