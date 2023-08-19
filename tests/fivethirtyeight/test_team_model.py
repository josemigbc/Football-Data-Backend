from django.test import TestCase
from fivethirtyeight.models import FootballTeam,FootballCompetition
from test_data import team_data_ok,competition_data_ok,team_data_without_national_league,team_data_with_another_id

class FootballTeamTest(TestCase):
    
    def setUp(self) -> None:
        self.competition = FootballCompetition.objects.create(**competition_data_ok)
        
    def test_create(self):
        team = FootballTeam.objects.create(**team_data_ok,national_league=self.competition)
        self.assertIsNotNone(FootballTeam.objects.all().first())
        self.assertEqual(team,FootballTeam.objects.get(pk=23))
        
    def test_create_without_fields(self):
        with self.assertRaises(Exception):
            FootballTeam.objects.create(**team_data_without_national_league)

    def test_same_name(self):
        FootballTeam.objects.create(**team_data_ok,national_league=self.competition)
        with self.assertRaises(Exception):
            FootballTeam.objects.create(**team_data_with_another_id,national_league=self.competition)