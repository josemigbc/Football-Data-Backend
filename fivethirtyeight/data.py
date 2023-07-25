import requests
from bs4 import BeautifulSoup,Tag,NavigableString
from .models import FootballCompetition


URL = "https://projects.fivethirtyeight.com/soccer-predictions"

def manage_competition(soup:Tag | NavigableString | None) -> dict:
    if not soup:
        return {}
    logo = soup.find('img')["src"]
    name = soup.find(class_="leagueName").text
    season = soup.find(class_="leagueDate").text
    season = season.split("-")[0]
    country = soup.find(class_="leagueCountry").text
    last_updated = soup.find(class_="timestamp").text
    return {
        "logo":f"https://projects.fivethirtyeight.com{logo}",
        "name": name,
        "country": country,
        "season": season,
        "last_updated": last_updated,
    }

def get_standings(league_name_url,season=2022) -> dict:
    url = f"https://projects.fivethirtyeight.com/soccer-predictions/forecasts/{season}_{league_name_url}_forecast.json"
    response = requests.get(url)
    if response.status_code != 200:
        return {}
    return response.json()

def get_competition(league_name_url:str) -> dict:
    url = f"{URL}/{league_name_url}/"
    response = requests.get(url)
    if response.status_code != 200:
        return {}
    soup = BeautifulSoup(response.content,features="html.parser")
    
    competition_soup = soup.find(class_="league-info")
    competition = manage_competition(competition_soup)
    
    standings = get_standings(league_name_url,season=competition.get("season"))
    
    id = standings.get("forecasts")[0].get("league_id") 
    competition.update({
        "id": id,
        "standings": standings,
        "name_url": league_name_url,
        "last_updated": standings.get("last_updated")
    })
    
    return competition
    
def manage_teams(soup:Tag | NavigableString | None) -> list[dict] | list[None]:
    if not soup:
        return []
    fields = ["rank",'','name','national_league','country','offensive','defensive','spi']
    teams_row_soup = soup.find_all('tr')
    data = []        
    for team in teams_row_soup:
        logo_soup = team.find(class_="logo")
        if logo_soup:
            logo = logo_soup.get("data-imgurl")
            id = logo.split("https://secure.espn.com/combiner/i?img=/i/teamlogos/soccer/500/")[1].split(".")[0]
            props = [ prop.text for prop in team.find_all('td')]
            team_data = dict(zip(fields,props))
            national_league_name = team_data.get("national_league").strip()
            try:
                national_league = FootballCompetition.objects.get(name=national_league_name).id
            except:
                national_league = None
            team_data.update({
                "id":int(id),
                "logo": logo,
                "national_league": national_league,
            })
            data.append(team_data)
    
    return data

def get_teams() -> list[dict] | list[None]:
    url = "https://projects.fivethirtyeight.com/soccer-predictions/global-club-rankings/"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    soup = BeautifulSoup(response.content,features="html.parser")
    teams_soup = soup.find(class_="all-teams")
    teams = manage_teams(teams_soup)
    return teams

def get_matches(league_name_url:str,season:int=2022) -> list[dict] | list[None]:
    url = f"https://projects.fivethirtyeight.com/soccer-predictions/forecasts/{season}_{league_name_url}_matches.json"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    matches = response.json()
    def manage_match(match:dict):
        match.update({
            "competition": match.get("league_id"),
            "team1": match.get("team1_id"),
            "team2": match.get("team2_id")
        })
        return match
    
    return list(map(manage_match,matches))
    

