from django.urls import path
from cride.users.views import UserLoginAPIView


urlpatterns = [
    path('users/login/', UserLoginAPIView.as_view(), name='login'),
]
