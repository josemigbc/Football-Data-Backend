from .models import FootballTeam
from .data import get_teams,get_matches,get_competition
from .serializers import FootballTeamSerializer,FootballMatchSerializer,FootballCompetitionSerializer

def update_competition(data):
    serializer = FootballCompetitionSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return True
    print(serializer.errors)
    return False

def update_teams(data):
    
    serializer = FootballTeamSerializer(data=data,many=True)
    if serializer.is_valid():
        print(serializer.validated_data)
        serializer.save()
        return True
    print(serializer.errors)
    return False

def update_matches(data):
    serializer = FootballMatchSerializer(data=data,many=True)
    if serializer.is_valid():
        serializer.save()
        return True
    print(serializer.errors[0])
    return False

def main():
    result = []
    amount_teams = FootballTeam.objects.all().count()
    if amount_teams < 10:
        teams = get_teams()
        r = update_teams(teams)
        result.append(r)
    else:
        result.append(None)
    
    LEAGUES = ["champions-league","bundesliga","premier-league","la-liga","ligue-1","serie-a"]
    for league in LEAGUES:
        competition = get_competition(league)
        r = update_competition(competition)
        result.append(r)
        matches = get_matches(league)
        r = update_matches(matches)
        result.append(r)
    
    