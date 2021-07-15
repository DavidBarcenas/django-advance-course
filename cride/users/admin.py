from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from cride.users.models import User, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin"""

    list_display = (
        'user',
        'reputation',
        'rides_taken',
        'rides_offered'
    )

    search_fields = (
        'user__username',
        'user__email',
        'user__first_name',
        'user__last_name'
    )

    list_filter = ('reputation',)

    fieldsets = (
        ('Profile', {
            'fields': (('user', 'picture', 'biography'))
        }),
        ('Stats', {
            'fields': (('rides_taken', 'rides_offered', 'reputation'))
        }),
        ('Metadata', {
            'fields': (('created', 'modified'))
        })
    )

    readonly_fields = ('created', 'modified')


class ProfileInline(admin.StackedInline):
    """Profile that will be created when a user is added."""

    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'


class CustomUserAdmin(UserAdmin):
    """User model admin"""

    inlines = (ProfileInline,)

    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'is_staff',
        'is_client'
    )

    list_filter = (
        'is_client',
        'is_staff',
        'created',
        'modified'
    )


admin.site.register(User, CustomUserAdmin)