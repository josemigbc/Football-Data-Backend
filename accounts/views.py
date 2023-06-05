from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class UserView(APIView):

    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data,status.HTTP_200_OK)
    
class UserCreationView(CreateAPIView):
    serializer_class = UserSerializer
        
    