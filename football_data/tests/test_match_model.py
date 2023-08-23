from django.test import TestCase
from football_data.models import Match
import datetime

class MatchTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.data = {"name": "Match Test"}
        cls.fields_data = {
            "id": 4000,
            "competition": "LT",
            "home_team_id": 1,
            "away_team_id": 2,
            "datetime": datetime.datetime(2023,6,10),
        }
    
    def test_create(self):
        Match.objects.create(**self.fields_data,data=self.data)
        match = Match.objects.all().get(id=4000)
        self.assertEqual(match.data,self.data)
        self.assertEqual(match.competition,"LT")
    
    def test_create_without_fields(self):
        
        with self.assertRaises(Exception):
            Match.objects.create(**self.fields_data)
        
        with self.assertRaises(Exception):
            Match.objects.create(data=self.data)
            
        with self.assertRaises(Exception):
            Match.objects.create()