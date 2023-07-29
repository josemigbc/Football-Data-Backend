from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.routers import SimpleRouter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import FootballCompetition,FootballMatch,FootballTeam
from .serializers import FootballCompetitionSerializer,FootballMatchSerializer,FootballTeamSerializer,FootballCompetitionForMatchAndTeamSerializer,FootballTeamNameSerializer

class FootballCompetitionViewSet(ReadOnlyModelViewSet):
    queryset = FootballCompetition.objects.all()
    serializer_class = FootballCompetitionSerializer
    
    def get_serializer_class(self):
        if self.action in ["list", "get_name"]:
            return FootballCompetitionForMatchAndTeamSerializer
        return super().get_serializer_class()
    
    @action(detail=True,methods=['get'])
    def get_name(self,request,pk=None):
        queryset = self.get_queryset()
        try:
            obj = queryset.get(pk=pk)
            serializer = self.get_serializer_class()(obj)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class FootballTeamViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    queryset = FootballTeam.objects.all()
    serializer_class = FootballTeamSerializer
    
    def get_serializer_class(self):
        if self.action == "get_name":
            return FootballTeamNameSerializer
        return super().get_serializer_class()
    
    @action(detail=True,methods=['get'])
    def get_name(self,request,pk=None):
        queryset = self.get_queryset()
        try:
            obj = queryset.get(pk=pk)
            serializer = self.get_serializer_class()(obj)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

class FootballMatchViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    queryset = FootballMatch.objects.all().order_by("datetime")
    serializer_class = FootballMatchSerializer
    
    def get_queryset(self):
        
        queryset = super().get_queryset()
        
        if self.action != 'list':
            return queryset
        
        team = self.request.GET.get('team')
        date = self.request.GET.get('date')
        competition = self.request.GET.get('competition')
        
        if date:
            queryset = queryset.filter(datetime__date=date)
        if team:
            queryset_home = queryset.filter(team1=team)
            queryset_away = queryset.filter(team2=team)
            queryset = queryset_home.union(queryset_away)
        if competition:
            queryset = queryset.filter(competition=competition)
        
        return queryset
    
    @action(detail=False,methods=['get'])
    def landing_match(self,request):
        match = self.get_queryset().filter(status="pre").first()
        if match:
            serializer = self.serializer_class(match)
            return Response(data=serializer.data)
        match = self.get_queryset().filter(status="post").order_by("-datetime").first()
        serializer = self.serializer_class(match)
        return Response(data=serializer.data)
        

router = SimpleRouter()
router.register(r'matches',FootballMatchViewSet)
router.register(r'teams',FootballTeamViewSet)
router.register(r'competitions',FootballCompetitionViewSet)

urlpatterns = router.urls