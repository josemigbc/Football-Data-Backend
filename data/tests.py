from rest_framework.test import APITestCase
from .models import Match,Team,Competition
from accounts.models import User
from balance.models import Balance
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from data.data_test import match_data,team_data1,team_data2,competition_data,team_data3
from data.data import save_match,save_competition,save_team,get_matches,competitions

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
    
    def test_get_match_by_id_exists(self):
        
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
    
    def test_get_404_by_match_id_doent_exist(self):
        
        response = self.client.get('/api/match/3/')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
        response = self.client.get('/api/match/10/')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
    def test_get_match_by_competition_exist(self):
        
        response = self.client.get("/api/match/competition/1/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),2)
    
    def test_get_match_by_competition_doesnt_exist(self):
        response = self.client.get("/api/match/competition/2/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),0)
        
        response = self.client.get("/api/match/competition/3/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),0)
    
    def test_get_match_by_date_with_matches(self):
        
        response = self.client.get("/api/match/date/2022/8/12/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        
        response = self.client.get("/api/match/date/2023/1/23/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
    
    def test_get_match_by_date_with_no_matches(self):
        
        response = self.client.get("/api/match/date/2022/8/15/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),0)
        
        response = self.client.get("/api/match/date/2022/12/12/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),0)
        
    def test_get_match_by_team_exist(self):
        
        response = self.client.get("/api/match/team/1/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),2)
        
        response = self.client.get("/api/match/team/2/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),2)
    
    def test_get_match_by_team_doesnt_exist(self):   
        response = self.client.get("/api/match/team/4/")
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
        response = self.client.get("/api/match/team/3/")
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_get_team_by_id_exist(self):
        
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
    
    def test_get_team_by_id_doesnt_exist(self):    
        response = self.client.get("/api/team/3/")
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
        response = self.client.get("/api/team/4/")
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
    def test_get_competition_by_id_exist(self):
        
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
    
    def test_get_competition_by_id_doesnt_exist(self):   
        response = self.client.get("/api/competition/3/")
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
        response = self.client.get("/api/competition/4/")
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
    
    def test_save_match_new(self):
        success = save_match(match_data.copy())
        match = Match.objects.get(id=match_data.get("id"))
        self.assertEqual(success,True)
        self.assertEqual(match.competition.id,match_data.get("competition",None).get("id",None))
        self.assertEqual(match.status,match_data.get("status",None))
        self.assertEqual(match.home_team.id,match_data.get("homeTeam",None).get("id",None))
    
    def test_save_match_modify(self):   
        match_data["fulltime_away"] = 5
        success = save_match(match_data.copy())
        match = Match.objects.get(id=match_data.get("id"))
        self.assertEqual(success,True)
        self.assertEqual(match.competition.id,match_data.get("competition",None).get("id",None))
        self.assertEqual(match.status,match_data.get("status"),None)
        self.assertEqual(match.home_team.id,match_data.get("homeTeam",None).get("id",None))
        self.assertEqual(match.fulltime_away,match_data.get("score",None).get("fullTime",None).get("away",None))
    
    def test_save_match_new_same_teams(self):   
        match_data["id"] = 5
        success = save_match(match_data.copy())
        self.assertEqual(success,True)
        match = Match.objects.get(id=match_data.get("id"))
        self.assertEqual(match.competition.id,match_data.get("competition",None).get("id",None))
        self.assertEqual(match.status,match_data.get("status",None))
        self.assertEqual(match.home_team.id,match_data.get("homeTeam",None).get("id",None))
        self.assertEqual(match.id,match_data.get("id",None))
    
    def test_save_match_new_with_no_team(self):    
        match_data["id"] = 4
        match_data.pop("homeTeam")
        success = save_match(match_data.copy())
        self.assertEqual(success,False)
        
    def test_save_team_new(self):
        success = save_team(team_data1)
        self.assertTrue(success)
        team = Team.objects.get(id=team_data1.get("id"))
        self.assertEqual(team.name,team_data1.get("name"))
        self.assertEqual(team.short_name,team_data1.get("short_name"))
        self.assertEqual(team.tla,team_data1.get("tla"))
        
        success = save_team(team_data2)
        self.assertEqual(success,True)
    
    def test_save_team_modify(self):   
        
        success = save_team(team_data3)
        team = Team.objects.get(id=team_data3.get("id"))
        self.assertTrue(success)
        self.assertEqual(team.name,team_data3.get("name"))
        self.assertEqual(team.short_name,team_data3.get("short_name"))
        self.assertEqual(team.tla,team_data3.get("tla"))
    
    def test_save_team_with_same_name(self):   
        team_data = team_data3.copy()
        team_data["id"] = 3
        success = save_team(team_data)
        self.assertFalse(success)
        
    def test_save_competition_new(self):
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
        
    """ def test_get_matches_api(self):
        for competition in competitions:
            success = get_matches(competition)
            self.assertEqual(success,True) """
        
        
        
        
        
        