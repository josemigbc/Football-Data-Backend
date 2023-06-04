from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OddsSerializer,GameSerializer
from .models import Game,Odds
from data.models import Match

# Create your views here.

class OddsRetrieve(APIView):
    def get(self,request,id):
        match = Match.objects.filter(id=id).first()
        if not match:
            return Response(status=status.HTTP_404_NOT_FOUND)
        odds = Odds.objects.filter(match=match,is_active=True).first()
        if odds:
            serializer = OddsSerializer(odds)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

class GameListCreateView(generics.ListCreateAPIView):
    serializer_class = GameSerializer
    
    def get_queryset(self):
        return Game.objects.filter(user=self.request.user)
    
class GameRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = GameSerializer


        

