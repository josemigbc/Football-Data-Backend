from .models import FootballTeam,FootballMatch
from .data import get_teams,get_matches,get_competition
from .serializers import FootballTeamForm,FootballMatchForm,FootballCompetitionSerializer

def update_competition(data):
    serializer = FootballCompetitionSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return True
    print(serializer.errors)
    return False

def update_teams(data):
    for team in iter(data):
        print(team)
        obj = FootballTeam.objects.filter(id=team["id"]).first()
        serializer = FootballTeamForm(instance=obj,data=team)
        if serializer.is_valid():
            serializer.save()
            print("OK")
    return True

def update_matches(data):
    for match in iter(data):
        obj = FootballMatch.objects.filter(id=match["id"]).first()
        serializer = FootballMatchForm(instance=obj,data=match)
        if serializer.is_valid():
            serializer.save()

def main():
    LEAGUES = ["bundesliga","premier-league","la-liga","ligue-1","serie-a","mls","eredivisie","primeira-liga","first-division-a","premiership"]
    for league in LEAGUES:
        competition = get_competition(league)
        r = update_competition(competition)
        print(f"{'OK' if r else 'Failed'}: {league}")
    
    teams = get_teams()
    update_teams(teams)
    
    for league in LEAGUES:    
        matches = get_matches(league)
        update_matches(matches)
        

#excute
#python manage.py shell
#>>> from fivethirtyeight.updater import main
#>>> main()
    
    