from django.test import TestCase
from django.utils import timezone
import datetime
from fivethirtyeight.models import FootballCompetition,FootballTeam,FootballMatch
from test_data import *

class FootballMatchTest(TestCase):
    def setUp(self) -> None:
        self.competition = FootballCompetition.objects.create(**competition_data_ok)
        self.team1 = FootballTeam.objects.create(**team_data_ok,national_league=self.competition)
        self.team2 = FootballTeam.objects.create(**team_data_ok2,national_league=self.competition)
        
    def test_create(self):
        now = timezone.now()
        pre_date = now - datetime.timedelta(days=10)
        post_date = now + datetime.timedelta(days=10)
        match_pre = FootballMatch.objects.create(**match_data_prematch_ok,competition=self.competition,team1=self.team1,team2=self.team2,datetime=pre_date)
        match_post = FootballMatch.objects.create(**match_data_postmatch_ok,competition=self.competition,team1=self.team1,team2=self.team2,datetime=post_date)
        
        self.assertEqual(FootballMatch.objects.all().count(),2)
        self.assertEqual(FootballMatch.objects.filter(competition=self.competition).count(),2)
        self.assertEqual(FootballMatch.objects.filter(datetime__gt=now).count(),1)
        
    def test_create_without_fields(self):
        with self.assertRaises(Exception):
            FootballMatch.objects.create(**match_data_without_team1,competition=self.competition,team2=self.team2,datetime=timezone.now())
        with self.assertRaises(Exception):
            FootballMatch.objects.create(**match_data_without_team2,competition=self.competition,team1=self.team1,datetime=timezone.now())
        with self.assertRaises(Exception):
            FootballMatch.objects.create(**match_data_without_competition,team1=self.team1,team2=self.team2,datetime=timezone.now())
        with self.assertRaises(Exception):
            FootballMatch.objects.create(**match_data_without_prob1,competition=self.competition,team1=self.team1,team2=self.team2,datetime=timezone.now())
        with self.assertRaises(Exception):
            FootballMatch.objects.create(**match_data_without_prob2,competition=self.competition,team1=self.team1,team2=self.team2,datetime=timezone.now())
        with self.assertRaises(Exception):
            FootballMatch.objects.create(**match_data_without_probtie,competition=self.competition,team1=self.team1,team2=self.team2,datetime=timezone.now())
        with self.assertRaises(Exception):
            FootballMatch.objects.create(**match_data_postmatch_ok,competition=self.competition,team1=self.team1,team2=self.team2,)
