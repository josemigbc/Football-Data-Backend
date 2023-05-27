import requests
from .models import Match,Team,Competition
from .serializers import MatchSerializer,TeamSerializer,CompetitionSerializer

competitions = ["FL1","BL1","PD","PL","SA","CL",]

url = "https://api.football-data.org/v4/competitions/"
headers = {'X-Auth-Token': '40ddfae19e684296ba3a3859b301e1aa'}

def save_team(team_data:dict):
    if not team_data:
        return False
    corrections = {
        "logo":team_data.get("crest",None),
        "short_name":team_data.get("shortName",None),
    }
    team_data.update(corrections)
    team = Team.objects.filter(id=team_data.get("id",None))
    serializer = TeamSerializer(team[0] if team else None,data=team_data)
    if serializer.is_valid():
        serializer.save()
        return True
    print(serializer.errors)
    return False

def save_competition(competition_data:dict) -> bool:
    if not competition_data:
        return False
    competition_data.update({"logo":competition_data.get("emblem",None)})
    competition = Competition.objects.filter(id=competition_data.get("id",None))
    serializer = CompetitionSerializer(competition[0] if competition else None,data=competition_data)
    if serializer.is_valid():
        serializer.save()
        return True
    print(serializer.errors)
    return False

def save_match(match_data:dict) -> bool:
    if not match_data:
        return False
    match = Match.objects.filter(id=match_data.get("id"))
    competition_data = match_data.get("competition",None)
    home_team_data = match_data.get("homeTeam",None)
    away_team_data = match_data.get("awayTeam",None)
    success = save_competition(competition_data),save_team(home_team_data),save_team(away_team_data)
    
    if not all(success):
        return False
    
    match_data["competition"] = competition_data.get("id",None)
    match_data["home_team"] = home_team_data.get("id",None)
    match_data["away_team"] = away_team_data.get("id",None)
    score = match_data.get("score",None)
    match_data["duration"] = score.get("duration",None)
    match_data["winner"] = score.get("winner",None)
    halftime = score.get("halfTime",None)
    fulltime = score.get("fullTime",None)
    match_data["halftime_home"] = halftime.get("home",None)
    match_data["halftime_away"] = halftime.get("away",None)
    match_data["fulltime_home"] = fulltime.get("home",None)
    match_data["fulltime_away"] = fulltime.get("away",None)
    match_data["referee"] = match_data.get("referees",None)[0].get("name",None) if match_data.get("referees",None) else None
    match_data["last_updated"] = match_data.get("lastUpdated",None)
    
    serializer = MatchSerializer(match[0] if match else None,data=match_data)
    if serializer.is_valid():
        serializer.save()
        return True
    print(serializer.errors)
    return False
    
    
def get_matches(league:str) -> None:
    response = requests.get(f"{url}{league}/matches/",headers=headers)
    if response.status_code != 200:
        return False
    data = response.json()
    matches = data.get('matches',None)
    for match in matches:
        save_match(match)
    return True 