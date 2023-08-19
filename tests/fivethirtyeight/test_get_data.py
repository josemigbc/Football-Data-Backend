from django.test import TestCase
from django.conf import settings
from unittest.mock import patch
from fivethirtyeight.data import get_competition,get_matches,get_standings,get_teams,manage_competition,manage_teams
from bs4 import BeautifulSoup
from test_data import *

# Create your tests here.

class DataGetTest(TestCase):
    
    def test_manage_teams_with_none(self):
        teams = manage_teams(None)
        self.assertIsInstance(teams,list)
        self.assertGreater(1,len(teams))
    
    @patch('fivethirtyeight.models.FootballCompetition.objects.get')
    def test_manage_teams_with_ok(self, mock_get):
        mocked_competition = mock_get.return_value
        mocked_competition.id = 1
        with open(settings.BASE_DIR / 'tests/fivethirtyeight/tests_soup/teams_soup.html') as file:
            soup = BeautifulSoup(file,"html.parser")
        
        data = manage_teams(soup)
    
        self.assertEqual(data,manage_teams_expected_data)
    
    @patch('requests.get')
    @patch('fivethirtyeight.data.manage_teams')   
    def test_get_teams_with_ok(self,mock_teams,mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.content = '<div><div class="all-teams"></div></div>'        
        mock_teams.return_value = manage_teams_expected_data
        data = get_teams()
        self.assertEqual(data,mock_teams.return_value)
    
    @patch('requests.get')
    def test_get_teams_with_request_failed(self,mock_get):
        mock_data = mock_get.return_value
        mock_data.status_code = 404
        data = get_teams()
        self.assertEqual(data,[])
        
    def test_manage_competition_with_none(self):
        competition = manage_competition(None)
        self.assertIsInstance(competition,dict)
        self.assertGreater(1,len(competition.keys()))
    
    def test_manage_competition_with_ok(self):
        with open(settings.BASE_DIR / 'tests/fivethirtyeight/tests_soup/competition_soup.html') as file:
            soup = BeautifulSoup(file,"html.parser")
        
        data = manage_competition(soup)

        self.assertEqual(data,manage_competition_expected_data)
    
    @patch('requests.get')
    def test_get_standings_with_request_failed(self,mock_get):
        mock_data = mock_get.return_value
        mock_data.status_code = 404
        data = get_standings('la-liga',2022)
        self.assertEqual(data,{})
        
    @patch('requests.get')
    def test_get_standings_with_ok(self,mock_get):
        mock_data = mock_get.return_value
        mock_data.status_code = 200
        mock_data.json.return_value = get_standings_expected_data
        data = get_standings('la-liga')
        self.assertEqual(data,get_standings_expected_data)
    
    @patch('requests.get')
    def test_get_competition_with_request_failed(self,mock_get):
        mock_data = mock_get.return_value
        mock_data.status_code = 404
        data = get_competition('la-liga')
        self.assertEqual(data,{})
    
    @patch('requests.get')
    @patch('fivethirtyeight.data.manage_competition')
    @patch('fivethirtyeight.data.get_standings')
    def test_get_competition_with_ok(self,mock_standings,mock_competition,mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.content = '<div><div class="league-info"></div></div>'
        mock_competition.return_value = manage_competition_expected_data.copy()
        mock_standings.return_value = get_standings_expected_data
        
        data = get_competition('test')
        self.assertEqual(data,get_competition_expected_data)
    
    @patch('requests.get')
    def test_get_matches_with_ok(self,mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = response_matches_data
        
        data = get_matches("la-liga",2022)
        self.assertEqual(data,get_matches_expected_data)
        
    @patch('requests.get')
    def test_get_matches_with_request_failed(self,mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 404
        
        data = get_matches("la-liga",2022)
        
        self.assertEqual(data,[])  