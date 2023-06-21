from rest_framework.generics import RetrieveAPIView,ListAPIView
from rest_framework.views import APIView
from .serializers import MatchSerializer,TeamSerializer,CompetitionSerializer,FTETeamSerializer
from .models import Match,Team,Competition,FTETeam
from rest_framework.response import Response
from rest_framework import status
import datetime 
# Create your views here.

class MatchRetrieveView(RetrieveAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    

class MatchCompetitionListView(ListAPIView):
    serializer_class = MatchSerializer
    
    def get_queryset(self):
        queryset = Match.objects.none()
        competition_id = self.kwargs.get("pk",None)
        if competition_id is not None:
            queryset = Match.objects.filter(competition=competition_id).order_by("-utcDate")
        return queryset

class MatchTeamListView(APIView):
    
    def get(self,request,pk):
        matches = Match.objects.filter(home_team=pk).union(Match.objects.filter(away_team=pk)).order_by("-utcDate")
        if not matches:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MatchSerializer(matches,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class MatchDateListView(ListAPIView):
    serializer_class = MatchSerializer
    
    def get_queryset(self):
        queryset = Match.objects.none()
        year = self.kwargs.get("year",None)
        month = self.kwargs.get("month",None)
        day = self.kwargs.get("day",None)
        date = datetime.date(year,month,day)
        
        if all([year,month,day]):
            queryset = Match.objects.filter(utcDate__date=date).order_by("-utcDate")
        return queryset

class TeamRetrieve(RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class CompetitionRetrieve(RetrieveAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

class FTETeamRetrieve(RetrieveAPIView):
    queryset = FTETeam.objects.all()
    serializer_class = FTETeamSerializer

