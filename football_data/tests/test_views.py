from rest_framework.test import APITestCase
from django.urls import reverse
from django.utils import timezone
import datetime
from unittest.mock import patch
from football_data.models import Competition,Match,Scorers,Standings

class CompetitionViewsTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        Competition.objects.create(
            slug="LT1",
            data={
                "name": "Liga Test 1"
            },
        )
    
    def test_list(self):
        url = reverse('competition-list')
        response = self.client.get(url,format='json')
        data = response.data
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(data),1)
        self.assertEqual(data[0].get("name"),"Liga Test 1")
    
    def test_detail(self):
        url = reverse('competition-detail',args=["LT1"])
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data.get("name"),"Liga Test 1")
        
    def test_detail_doesnot_exist(self):
        url = reverse('competition-detail',args=["LT2"])
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,404)
        
class MatchViewsTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        Match.objects.create(
            id=1000,
            competition="LT1",
            home_team_id=1,
            away_team_id=2,
            datetime=timezone.now(),
            data={
                "name":"Team data",
            }
        )
        
        Match.objects.create(
            id=1001,
            competition="LT1",
            home_team_id=1,
            away_team_id=3,
            datetime=timezone.now() - datetime.timedelta(days=5),
            data={
                "name":"Team data",
            }
        )
        
        Match.objects.create(
            id=1002,
            competition="LT1",
            home_team_id=2,
            away_team_id=3,
            datetime=timezone.now() + datetime.timedelta(days=3),
            data={
                "name":"Team data",
            }
        )
        
        cls.today = timezone.now().strftime("%Y-%m-%d")
    
    def test_list_by_date(self):
        url = reverse('match-list')
        response = self.client.get(url,data={"date": self.today},format='json')
        data = response.data
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(data),1)
        
    def test_list_by_team(self):
        url = reverse('match-list')
        response = self.client.get(url,data={"team": 1},format='json')
        data = response.data
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(data),2)
    
    def test_list_by_competition(self):
        url = reverse('match-list')
        response = self.client.get(url,data={"competition": "LT1"},format='json')
        data = response.data
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(data),3)
    
    def test_list_by_none(self):
        url = reverse('match-list')
        response = self.client.get(url,format='json')
        data = response.data
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(data),1)
    
    def test_detail(self):
        url = reverse('match-detail',args=[1000])
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,200)
    
    def test_detail_doesnot_exist(self):
        url = reverse('match-detail',args=[1])
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,404)


class StandingsViewsTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        Standings.objects.create(
            competition="LT1",
            data={
                "standings": ["Standings"]
            },
        )
    
    def test_list(self):
        url = reverse('standings-list')
        response = self.client.get(url,format='json')
        data = response.data
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(data),1)
        self.assertEqual(data[0].get("standings"),["Standings"])
    
    def test_detail(self):
        url = reverse('standings-detail',args=["LT1"])
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data.get("standings"),["Standings"])
        
    def test_detail_doesnot_exist(self):
        url = reverse('standings-detail',args=["LT2"])
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,404)
        
class ScorersViewsTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        Scorers.objects.create(
            competition="LT1",
            data={
                "scorers": ["Scorers"]
            },
        )
    
    def test_list(self):
        url = reverse('scorers-list')
        response = self.client.get(url,format='json')
        data = response.data
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(data),1)
        self.assertEqual(data[0].get("scorers"), ["Scorers"])
    
    def test_detail(self):
        url = reverse('scorers-detail',args=["LT1"])
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data.get("scorers"), ["Scorers"])
        
    def test_detail_doesnot_exist(self):
        url = reverse('scorers-detail',args=["LT2"])
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,404)
        
class UpdateViewTest(APITestCase):
    @patch('football_data.data.Data.update_all',return_value={'test':'test'})
    def test_update_with_token_ok(self,mock):
        url = reverse('update')
        response = self.client.get(url,format='json',headers={'Update-Token':'TEST'})
        mock.assert_called_once()
        self.assertEqual(response.status_code,200)
    
    def test_update_with_incorrect_token(self):
        url = reverse('update')
        response = self.client.get(url,format='json',headers={'Update-Token':'TE'})
        self.assertEqual(response.status_code, 403)
    
    @patch('football_data.data.Data.update_all',side_effect=Exception)
    def test_update_with_error(self,mock):
        url = reverse('update')
        response = self.client.get(url,format='json',headers={'Update-Token':'TEST'})
        mock.assert_called_once()
        self.assertEqual(response.status_code, 409)