from django.db import models
from django.db.models.deletion import CASCADE
from cride.utils.models import CRideModel

class Profile(CRideModel):
    """Profile model
    
    A profile holds a user's public data like biography, 
    picture and statistics.
    """

    user      = models.OneToOneField('users.User', on_delete=CASCADE)
    biography = models.TextField(max_length=256, blank=True)
    picture   = models.ImageField(
        'profile picture',
        upload_to = 'users/pictures/',
        blank = True,
        null = True
    )


    # stats
    rides_taken   = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)
    reputation    = models.FloatField(
        default = 0.0,
        help_text="User's reputation based on the rides taken and offered."
    )

    def __str__(self) -> str:
        return self.user