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
    for team in iter(data):
        serializer = FootballTeamSerializer(data=team)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            print("OK")
        print(serializer.errors)
    return True

def update_matches(data):
    serializer = FootballMatchSerializer(data=data,many=True)
    if serializer.is_valid():
        serializer.save()
        return True
    print(serializer.errors[0])
    return False

def main():
    LEAGUES = ["champions-league","bundesliga","premier-league","la-liga","ligue-1","serie-a"]
    for league in LEAGUES:
        competition = get_competition(league)
        r = update_competition(competition)
        print(f"{'OK' if r else 'Failed'}: {league}")
    
    amount_teams = FootballTeam.objects.all().count()
    if amount_teams < 10:
        teams = get_teams()
        r = update_teams(teams)
        print(r)
    else:
        print(False)
    for league in LEAGUES:    
        matches = get_matches(league)
        r = update_matches(matches)
        print(f"{'OK' if r else 'Failed'}: {league}")
#excute
#python manage.py shell
#>>> from fivethirtyeight.updater import main
#>>> main()
    
    