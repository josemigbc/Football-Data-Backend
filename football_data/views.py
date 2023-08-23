from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.routers import SimpleRouter
from rest_framework.exceptions import NotFound
from django.utils import timezone
from .models import Match,Competition,Standings,Scorers
from .serializers import DataSerializer

# Create your views here.

class CompetitionViewSet(ReadOnlyModelViewSet):
    
    queryset = Competition.objects.all()
    serializer_class = DataSerializer
    
    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            obj = self.queryset.get(slug=pk)
            return obj
        except Competition.DoesNotExist:
            raise NotFound('The competition doesnot exist')
    
    """ def list(self, request, *args, **kwargs):
        data = list(map(lambda x: x.data, self.queryset))
        return Response(data,status=status.HTTP_200_OK)
    
    def retrieve(self, request,pk, *args, **kwargs):
        obj = self.queryset.get(id=pk)
        data = obj.data
        return Response(data,status=status.HTTP_200_OK) """

class MatchViewSet(ReadOnlyModelViewSet):
    
    queryset = Match.objects.all()
    serializer_class = DataSerializer
    
    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            obj = self.queryset.get(id=pk)
            return obj
        except Match.DoesNotExist:
            raise NotFound('The match doesnot exist')
    
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
            queryset_home = queryset.filter(home_team_id=team)
            queryset_away = queryset.filter(away_team_id=team)
            queryset = queryset_home.union(queryset_away)
        if competition:
            queryset = queryset.filter(competition=competition)
        
        if not any([date,team,competition]):
            today = timezone.now().date()
            queryset = queryset.filter(datetime__date=today)
            
        return queryset

class StandingsViewSet(ReadOnlyModelViewSet):
    
    queryset = Standings.objects.all()
    serializer_class = DataSerializer
    
    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            obj = self.queryset.get(competition=pk)
            return obj
        except Standings.DoesNotExist:
            raise NotFound('The standings doesnot exist')
    
class ScorersViewSet(ReadOnlyModelViewSet):
    
    queryset = Scorers.objects.all()
    serializer_class = DataSerializer
    
    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            obj = self.queryset.get(competition=pk)
            return obj
        except Scorers.DoesNotExist:
            raise NotFound('The scorers doesnot exist')

router = SimpleRouter()
router.register(r"api/football_data/competition",CompetitionViewSet)
router.register(r"api/football_data/matches",MatchViewSet)
router.register(r"api/football_data/standings",StandingsViewSet)
router.register(r"api/football_data/scorers",ScorersViewSet)

urlpatterns = router.urls
