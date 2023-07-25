from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.routers import SimpleRouter
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import FootballCompetition,FootballMatch,FootballTeam
from .serializers import FootballCompetitionSerializer,FootballMatchSerializer,FootballTeamSerializer

class FootballCompetitionViewSet(ReadOnlyModelViewSet):
    queryset = FootballCompetition.objects.all()
    serializer_class = FootballCompetitionSerializer

class FootballTeamViewSet(ReadOnlyModelViewSet):
    queryset = FootballTeam.objects.all()
    serializer_class = FootballTeamSerializer
    

class FootballMatchViewSet(ReadOnlyModelViewSet):
    queryset = FootballMatch.objects.all()
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