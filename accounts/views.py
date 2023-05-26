from rest_framework.views import APIView
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class UserView(APIView):

    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data,status.HTTP_200_OK)
        
    