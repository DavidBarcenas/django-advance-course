from django.urls import path
from cride.circles.views import create_circle, list_circles


urlpatterns = [
    path('circles/', list_circles),
    path('circles/create/', create_circle)
]
