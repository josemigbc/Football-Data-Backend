from django.test import TestCase
from football_data.models import Standings

class StandingsTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.data = {"name": "League Test","standings":{}}
    
    def test_create(self):
        Standings.objects.create(competition="LT",data=self.data)
        standings = Standings.objects.all().filter(competition="LT").first()
        self.assertEqual(standings.data,self.data)
    
    def test_create_without_fields(self):
        
        with self.assertRaises(Exception):
            Standings.objects.create(competition="LT")
        
        with self.assertRaises(Exception):
            Standings.objects.create(data=self.data)
            
        with self.assertRaises(Exception):
            Standings.objects.create()