from rest_framework.test import APITestCase
from .models import Match,Team,Competition
from accounts.models import User
from balance.models import Balance
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from data.data import save_match,save_competition,save_team

# Create your tests here.
class DataTests(APITestCase):
    def setUp(self) -> None:
        
        user = User.objects.create(email="test@test.com",username="test",password="test")
        Balance.objects.create(user=user)
        token = AccessToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        
        liga1 = Competition.objects.create(id=1,name="Liga Test 1", type="LEAGUE",logo="/logotest1.png")
        liga2 = Competition.objects.create(id=2,name="Liga Test 2", type="LEAGUE",logo="/logotest2.png")
        
        team1 = Team.objects.create(id=1,name="Test United",short_name="Test Utd",tla="TU",logo="/logotest1.png")
        team2 = Team.objects.create(id=2,name="Test City",short_name="Test City",tla="TC",logo="/logotest2.png")
        
        Match.objects.create(
            id = 1,
            competition = liga1,
            utcDate = "2022-08-12T19:00:00Z",
            status = "FINISHED",
            matchday = 10,
            stage = "REGULAR",
            group = None,
            last_updated = "2022-08-12T19:00:00Z",
            winner = 'HOME_TEAM',
            duration = "REGULAR",
            fulltime_home = 6,
            fulltime_away = 3,
            halftime_home = 4,
            halftime_away = 0,
            referee = "Anthony Taylor",
            home_team = team1,
            away_team = team2
        )
        Match.objects.create(
            id = 2,
            competition = liga1,
            utcDate = "2023-01-23T19:00:00Z",
            status = "FINISHED",
            matchday = 29,
            stage = "REGULAR",
            group = None,
            last_updated = "2022-08-12T19:00:00Z",
            winner = 'AWAY_TEAM',
            duration = "REGULAR",
            fulltime_home = 2,
            fulltime_away = 1,
            halftime_home = 0,
            halftime_away = 0,
            referee = "Anthony Taylor",
            home_team = team2,
            away_team = team1
        )
        
        return super().setUp()
    
    def test_get_match_by_id(self):
        
        response = self.client.get("/api/match/1/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"),1)
        self.assertEqual(response.data.get("home_team"),1)
        self.assertEqual(response.data.get("away_team"),2)
        self.assertEqual(response.data.get("fulltime_home"),6)
        self.assertEqual(response.data.get("fulltime_away"),3)
        
        response = self.client.get("/api/match/2/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"),2)
        self.assertEqual(response.data.get("home_team"),2)
        self.assertEqual(response.data.get("away_team"),1)
        self.assertEqual(response.data.get("fulltime_home"),2)
        self.assertEqual(response.data.get("fulltime_away"),1)
    
    def test_get_404_by_match_id(self):
        
        response = self.client.get('/api/match/3/')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
        response = self.client.get('/api/match/10/')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
    def test_get_match_by_competition(self):
        
        response = self.client.get("/api/match/competition/1/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),2)
        
        response = self.client.get("/api/match/competition/2/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),0)
        
        response = self.client.get("/api/match/competition/3/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),0)
    
    def test_get_match_by_date(self):
        
        response = self.client.get("/api/match/date/2022/8/12/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        
        response = self.client.get("/api/match/date/2023/1/23/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        
        response = self.client.get("/api/match/date/2022/8/15/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),0)
        
        response = self.client.get("/api/match/date/2022/12/12/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),0)
        
    def test_get_match_by_team(self):
        
        response = self.client.get("/api/match/team/1/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),2)
        
        response = self.client.get("/api/match/team/2/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),2)
        
        response = self.client.get("/api/match/team/4/")
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
        response = self.client.get("/api/match/team/3/")
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_get_team_by_id(self):
        
        response = self.client.get("/api/team/1/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"),1)
        self.assertEqual(response.data.get("name"),"Test United")
        self.assertEqual(response.data.get("tla"),"TU")
        
        response = self.client.get("/api/team/2/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"),2)
        self.assertEqual(response.data.get("name"),"Test City")
        self.assertEqual(response.data.get("tla"),"TC")
        
        response = self.client.get("/api/team/3/")
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
        response = self.client.get("/api/team/4/")
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
    def test_get_competition_by_id(self):
        
        response = self.client.get("/api/competition/1/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"),1)
        self.assertEqual(response.data.get("name"),"Liga Test 1")
        self.assertEqual(response.data.get("type"),"LEAGUE")
        
        response = self.client.get("/api/competition/2/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"),2)
        self.assertEqual(response.data.get("name"),"Liga Test 2")
        self.assertEqual(response.data.get("type"),"LEAGUE")
        
        response = self.client.get("/api/competition/3/")
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
        response = self.client.get("/api/competition/4/")
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
    
    def test_save_match(self):
        match_data = {
            "id": 2,
            "competition": {
                "id":10,
                "name": "Liga Test 10",
                "type": "ELIMINATORIES",
                "logo": "/logo.png",
            },
            "utcDate": "2022-01-23T19:00:00Z",
            "status": "IN_PLAY",
            "matchday": 28,
            "stage": "FINAL",
            "group": "GROUP_B",
            "last_updated": "2022-09-12T19:00:00Z",
            "winner":'DRAW',
            "duration": "EXTRA_TIME",
            "fulltime_home": 2,
            "fulltime_away": 2,
            "halftime_home": 1,
            "halftime_away": 1,
            "referee": "Michael Oliver",
            "home_team": {
                "id":10,
                "name": "Test FC",
                "short_name": "Test FC",
                "tla": "TFC",
                "logo": "/logo.png",
            },
            "away_team": {
                "id":11,
                "name": "Test UD",
                "short_name": "Test UD",
                "tla": "TUD",
                "logo": "/logo.png",
            },
        }
        
        success = save_match(match_data.copy())
        match = Match.objects.get(id=2)
        self.assertEqual(success,True)
        self.assertEqual(match.competition.id,match_data.get("competition",None).get("id",None))
        self.assertEqual(match.status,match_data.get("status",None))
        self.assertEqual(match.home_team.id,match_data.get("home_team",None).get("id",None))
        
        match_data["fulltime_away"] = 5
        success = save_match(match_data.copy())
        match = Match.objects.get(id=2)
        self.assertEqual(success,True)
        self.assertEqual(match.competition.id,match_data.get("competition",None).get("id",None))
        self.assertEqual(match.status,match_data.get("status"),None)
        self.assertEqual(match.home_team.id,match_data.get("home_team",None).get("id",None))
        self.assertEqual(match.fulltime_away,match_data.get("fulltime_away",None))
        
        match_data["id"] = 5
        success = save_match(match_data.copy())
        self.assertEqual(success,True)
        match = Match.objects.get(id=5)
        self.assertEqual(match.competition.id,match_data.get("competition",None).get("id",None))
        self.assertEqual(match.status,match_data.get("status",None))
        self.assertEqual(match.home_team.id,match_data.get("home_team",None).get("id",None))
        self.assertEqual(match.id,match_data.get("id",None))
        
        match_data["id"] = 4
        match_data.pop("home_team")
        success = save_match(match_data.copy())
        self.assertEqual(success,False)
        
    def test_save_team(self):
        team_data = {
            "id":1,
            "name": "Test Town",
            "short_name": "Test Town",
            "tla": "TTW",
            "logo": "/logo.png",
        }
        
        success = save_team(team_data)
        team = Team.objects.get(id=team_data.get("id"))
        self.assertEqual(success,True)
        self.assertEqual(team.name,team_data.get("name"))
        self.assertEqual(team.short_name,team_data.get("short_name"))
        self.assertEqual(team.tla,team_data.get("tla"))
        
        team_data["short_name"] = "TT"
        success = save_team(team_data)
        team = Team.objects.get(id=team_data.get("id"))
        self.assertEqual(success,True)
        self.assertEqual(team.name,team_data.get("name"))
        self.assertEqual(team.short_name,team_data.get("short_name"))
        self.assertEqual(team.tla,team_data.get("tla"))
        
        team_data["id"] = 3
        success = save_team(team_data)
        self.assertEqual(success,False)
        
        team_data = {
            "id":3,
            "name": "Test Wolves",
            "short_name": "Wolves",
            "tla": "TW",
            "logo": "/logo.png",
        }
        
        team_data["id"] = 3
        success = save_team(team_data)
        self.assertEqual(success,True)
        
    def test_save_competition(self):
        
        competition_data = {
            "id":1,
            "name": "Liga Test 3",
            "type": "ELIMINATORIES",
            "logo": "/logo.png",
        }
        
        success = save_competition(competition_data)
        competition = Competition.objects.get(id=competition_data.get("id"))
        self.assertEqual(success,True)
        self.assertEqual(competition.name,competition_data.get("name"))
        self.assertEqual(competition.type,competition_data.get("type"))
        
        competition_data["name"] = "Liga Test 3.1"
        success = save_competition(competition_data)
        competition = Competition.objects.get(id=competition_data.get("id"))
        self.assertEqual(success,True)
        self.assertEqual(competition.name,competition_data.get("name"))
        self.assertEqual(competition.type,competition_data.get("type"))
        
        competition_data["id"] = 3
        success = save_competition(competition_data)
        self.assertEqual(success,True)
        
        
        
        
        
        