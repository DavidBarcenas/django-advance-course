from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from cride.circles.serializers.circles import CircleModelSerializer
from cride.circles.models.circles import Circle
from cride.users.permissions import IsAccountOwner
from cride.users.models.users import User
from cride.users.serializers import (
    UserLoginSerializer, 
    UserModelSerializer, 
    UserSignUpSerializer,
    AccountVerificationSerializer
)

class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """User view set
    
    Handle sign up, login and account verification.
    """

    queryset = User.objects.filter(is_active=True, is_client=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        """Asign permissions based on action."""

        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action == 'retrieve':
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]

        return [p() for p in permissions]




    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        data = UserModelSerializer(user).data,

        return Response(data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """View to verify the token."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {'message': 'Congratulations, now go share some rides!'}

        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """Add extra data to the response."""
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        circles = Circle.objects.filter(members=request.user, membership__is_active=True)

        data = {
            'user': response.data,
            'circles': CircleModelSerializer(circles, many=True).data
        }
        response.data = data
        return response