from django.conf import settings
from django.db import transaction
import time
import requests
from .models import Competition,Match,Standings,Scorers


URL = settings.FOOTBALL_DATA_URL
headers = {'X-Auth-Token': settings.FOOTBALL_DATA_API_KEY}

class Data:
    competitions = ["FL1","BL1","PD","PL","SA","CL","ELC","PPL"]
    
    def do_get(self,endpoint):
        response = requests.get(f"{URL}/{endpoint}",headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise requests.exceptions.RequestException("The request wasn't successful")
    
    def get_competition(self,endpoint):
        competition = Competition.objects.filter(slug=endpoint).first()
        if competition:
            return False, "already exists"
        data:dict = self.do_get(endpoint)
        if not data:
            raise ValueError("Data must be a dict from json response")
        Competition.objects.create(slug=endpoint,data=data)
        return True, "created"
        
    def get_matches(self,competition):
        
        data:dict = self.do_get(f"{competition}/matches")
        if not data:
            raise ValueError("Data must be a dict from json response")
        matches_data:list[dict] = data.get("matches")
        
        for match in iter(matches_data):
            datetime = match.get("utcDate")
            id = match.get('id')
            
            match_obj = Match.objects.filter(id=id).first()
            if match_obj:
                match_obj.datetime = datetime
                match_obj.data = match
                match_obj.save()
            else:  
                home_team_id = match.get("homeTeam").get("id")
                away_team_id = match.get("awayTeam").get("id")    

                Match.objects.create(
                    id=id,
                    datetime=datetime,
                    home_team_id=home_team_id,
                    away_team_id=away_team_id,
                    competition=competition,
                    data=match,
                )
    
    def get_standings(self,competition):
    
        data:dict = self.do_get(f"{competition}/standings")
        
        if not data:
            raise ValueError("Data must be a dict from json response")
        standings:list[dict] = data.get("standings")
        standings_obj = Standings.objects.filter(competition=competition).first()
        
        if standings_obj:
            standings_obj.data = standings
            standings_obj.save()
            return True, "updated"
        
        Standings.objects.create(competition=competition,data=standings)
        return True, "created"
    
    def get_scorers(self,competition):
    
        data:dict = self.do_get(f"{competition}/scorers")
        
        if not data:
            raise ValueError("Data must be a dict from json response")
        scorers:list[dict] = data.get("scorers")
        
        scorers_obj = Scorers.objects.filter(competition=competition).first()
        if scorers_obj:
            scorers_obj.data = scorers
            scorers_obj.save()
            return True, "updated"
        
        Scorers.objects.create(competition=competition,data=scorers)
        return True, "created"
        
    def update(self,competition):
        try:
            with transaction.atomic():
                self.get_competition(competition)
                self.get_matches(competition)
                self.get_standings(competition)
                self.get_scorers(competition)
            r = f"{competition} ok"
            print(r)
            return True
        except Exception as err:
            print(err)
            
    def update_all(self):
        for competition in self.competitions:
            self.update(competition)
            time.sleep(60)        