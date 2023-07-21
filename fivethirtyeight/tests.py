from django.test import TestCase
from .data import get_competition,get_matches,get_standings,get_teams,manage_competition,manage_teams
from .models import FootballCompetition,FootballMatch,FootballTeam
from .updater import update_matches,update_competition,update_teams
from .tests_data import *
from django.utils import timezone
import datetime

LEAGUES = ["champions-league","bundesliga","premier-league","la-liga","ligue-1","serie-a"]
# Create your tests here.
class DataGetTest(TestCase):
    def test_get_competition(self):
        competition = get_competition("la-liga")
        self.assertIsInstance(competition,dict)
        keys = competition.keys()
        self.assertIn("name_url",keys)
        self.assertIn("standings",keys)
        self.assertIn("country",keys)
    
    def test_get_matches(self):
        matches = get_matches("serie-a")
        self.assertIsInstance(matches,list)
        self.assertIsInstance(matches[0],dict)
        self.assertIn("id",matches[0].keys())
    
    def test_get_standings(self):
        standings = get_standings("bundesliga")
        self.assertIsInstance(standings,dict)
        self.assertIsInstance(standings.get("forecasts"),list)
            
    def test_get_teams(self):
        teams = get_teams()
        self.assertIsInstance(teams,list)
        self.assertGreater(len(teams),1)
        self.assertIsInstance(teams[0],dict)
    
    def test_manage_teams(self):
        teams = manage_teams(None)
        self.assertIsInstance(teams,list)
        self.assertGreater(1,len(teams))
        
    def test_manage_competition(self):
        competition = manage_competition(None)
        self.assertIsInstance(competition,dict)
        self.assertGreater(1,len(competition.keys()))
        
class FootballCompetitionTest(TestCase):
    def test_create(self):
        competition = FootballCompetition.objects.create(**competition_data_ok)
        
        self.assertIsNotNone(FootballCompetition.objects.all().first())
        self.assertEqual(competition,FootballCompetition.objects.get(pk=340))
    
    def test_same_name(self):
        FootballCompetition.objects.create(**competition_data_ok)
        
        with self.assertRaises(Exception):
            FootballCompetition.objects.create(**competition_data_with_another_id)
            
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

class UpdaterTests(TestCase):
    def setUp(self) -> None:
        self.competition = FootballCompetition.objects.create(
            id=243,
            name="Premier League",
            country="England",
            logo='https://projects.fivethirtyeight.com/soccer-predictions/images/la-liga-logo.png?v=16d33bfb',
            season=2022,
            last_updated='2023-06-04T21:06:46Z',
            name_url = 'premier-league'
        )
        FootballTeam.objects.create(
            id=97,
            name="Team Test 1",
            rank=3,
            national_league = self.competition, 
            offensive=2.8,
            defensive= 0.3, 
            spi=92.0,
            logo='https://secure.espn.com/combiner/i?img=/i/teamlogos/soccer/500/97.png&w=56',
        )
        FootballTeam.objects.create(
            id=247,
            name="Team Test 2",
            rank=4,
            national_league = self.competition, 
            offensive=2.8,
            defensive= 0.3, 
            spi=92.0,
            logo='https://secure.espn.com/combiner/i?img=/i/teamlogos/soccer/500/247.png&w=56',
        )
        
        
    def test_update_competiton(self):
        r = update_competition(competition_update)
        competition = FootballCompetition.objects.all().last()
        self.assertTrue(r)
        self.assertEqual(competition.name,"La Liga")
        self.assertEqual(competition.id,1869)
    
    def test_update_matches(self):
        r = update_matches(match_data_update)
        self.assertTrue(r)
        
        
    def test_update_teams(self):
        r = update_teams(teams_update)
        ids = list(FootballTeam.objects.all().values_list('id').order_by('id'))
        espected_ids = [(i,) for i in range(10,31)] + [(97,),(247,)]
        self.assertTrue(r)
        self.assertEqual(FootballTeam.objects.all().count(),23)
        self.assertEqual(ids,espected_ids)