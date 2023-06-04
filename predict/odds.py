import requests
from bs4 import BeautifulSoup
from predict.serializers import OddsSerializer
from data.models import Match,Team
import datetime
import math

competitions = ["champions-league","bundesliga","premier-league","la-liga","ligue-1","serie-a"]
url = "https://projects.fivethirtyeight.com/predicciones-de-futbol/"

def manage_data(match):
    if not match:
        return None

    teams_soup = match.find_all(class_="team")
    if not teams_soup:
        return None
    home_team,away_team = (team.text for team in teams_soup) if len(teams_soup) == 2 else (None,None)
    
    probs_soup = match.find_all(class_="prob")
    if not probs_soup:
        return None
    prob_home,prob_draw,prob_away = (prob.text.replace("%","") for prob in probs_soup) if len(probs_soup) == 3 else (None,None,None)
    
    if not all([home_team,away_team,prob_home,prob_draw,prob_away]):
        return None

    return {
            "home_team":home_team,
            "away_team":away_team,
            "odds_HOME": round(100/int(prob_home),2),
            "odds_DRAW": round(100/int(prob_draw),2),
            "odds_AWAY": round(100/int(prob_away),2),
        }

def save_odds(match):
    if not match:
        return False
    match_object = Match.objects.filter(home_team__fte_name__name=match.get("home_team",None),away_team__fte_name__name=match.get("away_team"),utcDate__gt=datetime.datetime.now()).first()
    match["match"] = match_object.id if match_object else None
    serializer = OddsSerializer(data=match)
    if serializer.is_valid():
        serializer.save()
        return True
    print(serializer.errors)
    return False

def get_probs(league:str):
    response = requests.get(f"{url}{league}/")
    if response.status_code != 200:
        return False
    data = response.content
    soup = BeautifulSoup(data,features="html.parser")
    matches = soup.find_all(class_="match_container")
    odds = [ manage_data(match) for match in matches ]
    success = [ save_odds(odd) for odd in odds ]
    return True


        
    
        