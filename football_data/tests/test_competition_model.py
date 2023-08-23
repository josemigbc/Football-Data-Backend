from django.test import TestCase
from football_data.models import Competition

class CompetitionTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.data = {"name": "League Test"}
    
    def test_create(self):
        Competition.objects.create(slug="LT",data=self.data)
        competiton = Competition.objects.all().filter(slug="LT").first()
        self.assertEqual(competiton.data,self.data)
    
    def test_create_without_fields(self):
        
        with self.assertRaises(Exception):
            Competition.objects.create(slug="LT")
        
        with self.assertRaises(Exception):
            Competition.objects.create(data=self.data)
            
        with self.assertRaises(Exception):
            Competition.objects.create()
        
