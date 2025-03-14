from .serializers import RegisterSerializer,LoginSerializer,LogoutSerializer
from .services import register_user,login_user,logout_user
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet

# Create your views here.
class AuthViewSet(ViewSet):

    def register(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = register_user(serializer.validated_data)
            return Response(RegisterSerializer(user).data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def login(self,request):
        serializer= LoginSerializer(data=request.data)
        if serializer.is_valid():
            session = login_user(serializer.validated_data["username"],serializer.validated_data["password"])
            return Response(session,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def logout(self,request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            logout_user(serializer.validated_data['refresh_token'])
            return Response(status=status.HTTP_205_RESET_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)