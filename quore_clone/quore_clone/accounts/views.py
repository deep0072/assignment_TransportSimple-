from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken 
from django.contrib.auth import authenticate
from rest_framework.views import APIView


from accounts.models import UserModel
from accounts.serializers import (
    RegisterSerializer, UserSerializer
)



        
class RegisterView(APIView):
   def post(self, request):
       serializer = RegisterSerializer(data=request.data)
       try:
           if serializer.is_valid(raise_exception=True):               
               serializer.save()
               return Response({"message":"created successfully", "data":serializer.data}, status=status.HTTP_201_CREATED)  
       except Exception as e:
           return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
      


class CustomLoginView(APIView):
    """
    Custom API endpoint for user login using email and password.
   
    """

    def post(self, request, *args, **kwargs):
      
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Both email and password are required.'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=email, password=password)

        if user is not None:
     
            if user.is_active:

               
                refresh = RefreshToken.for_user(user)

                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
              
                return Response({'error': 'User account is disabled.'},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """

    Expects the refresh token in the request body to logout the user.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)         
            token.blacklist()
           
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
             return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": "Logout failed.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)