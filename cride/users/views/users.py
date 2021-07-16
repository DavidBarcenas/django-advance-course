from rest_framework.views import APIView
from rest_framework import status

from cride.users.serializers import UserLoginSerializer


class UserLoginAPIView(APIView):
    """User Login API View"""
    
    def post(self,request, *args, **kwargs):
        """Handle HTTP POST request"""

        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.save()
        data = {
            'status': 'ok',
            'token': token
        }

        return Response(data, status=status.HTTP_201_CREATED)