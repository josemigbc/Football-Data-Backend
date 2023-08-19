from django.test import TestCase
from fivethirtyeight.models import FootballCompetition
from test_data import competition_data_ok, competition_data_with_another_id

class FootballCompetitionTest(TestCase):
    def test_create(self):
        competition = FootballCompetition.objects.create(**competition_data_ok)
        self.assertIsNotNone(FootballCompetition.objects.all().first())
        self.assertEqual(competition,FootballCompetition.objects.get(pk=340))
    
    def test_same_name(self):
        FootballCompetition.objects.create(**competition_data_ok)
        
        with self.assertRaises(Exception):
            FootballCompetition.objects.create(**competition_data_with_another_id)