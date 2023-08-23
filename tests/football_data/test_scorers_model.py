from django.test import TestCase
from football_data.models import Scorers

class ScorersTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.data = {"name": "League Test","scorers":{}}
    
    def test_create(self):
        Scorers.objects.create(competition="LT",data=self.data)
        scorers = Scorers.objects.all().filter(competition="LT").first()
        self.assertEqual(scorers.data,self.data)
    
    def test_create_without_fields(self):
        
        with self.assertRaises(Exception):
            Scorers.objects.create(competition="LT")
        
        with self.assertRaises(Exception):
            Scorers.objects.create(data=self.data)
            
        with self.assertRaises(Exception):
            Scorers.objects.create()