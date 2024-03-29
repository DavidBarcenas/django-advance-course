from django.db import models
from django.db.models.deletion import SET_NULL
from cride.utils.models import CRideModel


class Ride(CRideModel):
    offered_by = models.ForeignKey('users.User', on_delete=SET_NULL, null=True)
    offered_in = models.ForeignKey('circles.Circle', on_delete=SET_NULL, null=True)

    passengers = models.ManyToManyField("users.User", related_name='passengers')

    available_seats = models.PositiveSmallIntegerField(default=1)
    comments = models.TextField(blank=True)

    departure_location = models.CharField(max_length=255)
    departure_date = models.DateTimeField()
    arrival_location = models.CharField(max_length=255)
    arrival_date = models.DateTimeField()

    rating = models.FloatField(null=True)

    is_active = models.BooleanField(
        'active_status',
        default = True,
        help_text = 'Used for disabing the ride or making it as finished.'
    )

    def __str__(self):
        """Return ride details"""
        return '{_from} to {_to} | {day} {i_time} - {f_time}'.format(
            _from = self.departure_location,
            to = self.arrival_location,
            day = self.departure_date.strftime('%a %d, %b'),
            i_time = self.departure_date.strftime('%I:%M %p'),
            f_time = self.arrival_date.strftime('%I:%M %p'),
        )