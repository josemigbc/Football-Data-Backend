from rest_framework.test import APITestCase
from rest_framework import status
from predict.odds import manage_data,save_odds,get_probs
from data.models import Match,Team,Competition,FTETeam
from data.data_test import team_data1,team_data2
from predict.data_test import match1,match1_result,match2,match3,match4,match5,match2_result,match3_result
from bs4 import BeautifulSoup
from .models import Odds,Game
from accounts.models import User
from balance.models import Balance
from rest_framework_simplejwt.tokens import AccessToken

# Create your tests here.
class PredictTests(APITestCase):
    
    def setUp(self) -> None:
        
        user = User.objects.create(email="test@test.com",username="test",password="test")
        Balance.objects.create(user=user)
        token = AccessToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        
        liga1 = Competition.objects.create(id=1,name="Liga Test 1", type="LEAGUE",logo="/logotest1.png")
        
        fte_name1 = FTETeam.objects.create(name="Test Utd")
        fte_name2 = FTETeam.objects.create(name="Test City")
        
        team1 = Team.objects.create(id=1,name="Test United",short_name="Test Utd",tla="TU", fte_name=fte_name1,logo="/logotest1.png")
        team2 = Team.objects.create(id=2,name="Test City",short_name="Test City",tla="TC",fte_name=fte_name2,logo="/logotest2.png")
        team3 = Team.objects.create(id=3,name="Football Club Test",short_name="FC Test",tla="FCT",logo="/logotest3.png")
        team4 = Team.objects.create(id=4,name="Union Deportiva Test",short_name="UD Test",tla="UDT",logo="/logotest4.png")
        
        match_test1 =Match.objects.create(
            id = 1,
            competition = liga1,
            utcDate = "2023-04-30T19:00:00Z",
            status = "FINISHED",
            matchday = 10,
            stage = "REGULAR",
            group = None,
            last_updated = "2022-08-12T19:00:00Z",
            winner = "HOME_TEAM",
            duration = "REGULAR",
            fulltime_home = 4,
            fulltime_away = 0,
            halftime_home = 6,
            halftime_away = 3,
            referee = "Anthony Taylor",
            home_team = team2,
            away_team = team3,
        )
        match_test2 = Match.objects.create(
            id = 2,
            competition = liga1,
            utcDate = "2023-06-23T19:00:00Z",
            status = "SCHEDULED",
            matchday = 29,
            stage = "REGULAR",
            group = None,
            last_updated = "2022-08-12T19:00:00Z",
            winner = None,
            duration = "REGULAR",
            fulltime_home = None,
            fulltime_away = None,
            halftime_home = None,
            halftime_away = None,
            referee = "Anthony Taylor",
            home_team = team2,
            away_team = team1
        )
        match_test3 = Match.objects.create(
            id = 3,
            competition = liga1,
            utcDate = "2023-06-23T19:00:00Z",
            status = "SCHEDULED",
            matchday = 29,
            stage = "REGULAR",
            group = None,
            last_updated = "2022-08-12T19:00:00Z",
            winner = None,
            duration = "REGULAR",
            fulltime_home = None,
            fulltime_away = None,
            halftime_home = None,
            halftime_away = None,
            referee = "Anthony Taylor",
            home_team = team4,
            away_team = team1,
        )
        
        match_test4 = Match.objects.create(
            id = 4,
            competition = liga1,
            utcDate = "2023-06-23T19:00:00Z",
            status = "SCHEDULED",
            matchday = 29,
            stage = "REGULAR",
            group = None,
            last_updated = "2022-08-12T19:00:00Z",
            winner = None,
            duration = "REGULAR",
            fulltime_home = None,
            fulltime_away = None,
            halftime_home = None,
            halftime_away = None,
            referee = "Anthony Taylor",
            home_team = team3,
            away_team = team4,
        )
        
        self.match1 = match_test1
        self.match2 = match_test2
        self.match3 = match_test3
        
        game1 = Game.objects.create(
            user = user,
            match = match_test2,
            amount = 10,
            winner = '1',
            odds_HOME = 2.50,
            odds_DRAW = 4.30,
            odds_AWAY = 7.20,
        )
        
        game2 = Game.objects.create(
            user = user,
            match = match_test3,
            amount = 16,
            winner = '2',
            odds_HOME = 1.50,
            odds_DRAW = 2.30,
            odds_AWAY = 3.20,
        )
        
        odds1 = Odds.objects.create(
            match = match_test2,
            odds_HOME = 2.00,
            odds_DRAW = 4.34,
            odds_AWAY = 3.15,
            is_active = True,
        )
        
        return super().setUp()
    
    def test_manage_data_with_match_ok(self):
        soup = BeautifulSoup(match1,features="html.parser")
        data = manage_data(soup)
        self.assertEqual(match1_result,data)
    
    def test_manage_data_with_match_without_a_team(self):
        soup = BeautifulSoup(match2,features="html.parser")
        data = manage_data(soup)
        self.assertIsNone(data)
        
    
    def test_manage_data_with_match_with_incorrect_class_container(self):
        soup = BeautifulSoup(match3,features="html.parser")
        data = manage_data(soup)
        self.assertEqual(match1_result,data)
    
    def test_manage_data_with_empty_match(self):
        soup = BeautifulSoup(match4,features="html.parser")
        data = manage_data(soup)
        self.assertIsNone(data)
    
    def test_manage_data_without_data_in_div(self):
        soup = BeautifulSoup(match5,features="html.parser")
        data = manage_data(soup)
        self.assertIsNone(data)
        
    def test_save_odds_with_data_ok(self):
        success = save_odds(match3_result)
        self.assertTrue(success)
    
    def test_save_odds_with_empty(self):
        success = save_odds({})
        self.assertFalse(success)
    
    def test_save_odds_without_a_field(self):
        success = save_odds(match2_result)
        self.assertFalse(success)
    
    def test_game_list_view(self):
        response = self.client.get("/api/game/")
        self.assertEqual(status.HTTP_200_OK,response.status_code)
        self.assertEqual(len(response.data),2)
    
    def test_game_create_view_with_ok(self):
        data = {
            "user": 1,
            "match": 2,
            "amount": 5,
            "winner": "1",
            "odds_HOME": 3.00,
            "odds_DRAW": 4.50,
            "odds_AWAY": 2.45,
        }
        response = self.client.post("/api/game/",data=data)
        self.assertEqual(status.HTTP_201_CREATED,response.status_code)
    
    def test_game_create_view_without_a_field(self):
        data = {
            "user": 1,
            "match": 2,
            "amount": 5,
            "winner": "1",
            "odds_HOME": 3.00,
            "odds_DRAW": 4.50,
        }
        response = self.client.post("/api/game/",data=data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST,response.status_code)
    
    def test_game_create_view_with_empty(self):
        response = self.client.post("/api/game/",data={})
        self.assertEqual(status.HTTP_400_BAD_REQUEST,response.status_code)
    
    def test_odds_view_with_ok(self):
        response = self.client.get("/api/odds/2/")
        self.assertEqual(status.HTTP_200_OK,response.status_code)
        self.assertEqual(2,response.data.get("match"))
        self.assertEqual(2.0,response.data.get("odds_HOME"))
        
    def test_odds_view_with_match_doesnt_exist(self):
        response = self.client.get("/api/odds/5/")
        self.assertEqual(status.HTTP_404_NOT_FOUND,response.status_code)
    
    def test_odds_view_with_match_exist_odds_not(self):
        response = self.client.get("/api/odds/1/")
        self.assertEqual(status.HTTP_204_NO_CONTENT,response.status_code)