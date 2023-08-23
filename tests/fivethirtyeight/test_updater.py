from django.test import TestCase
from fivethirtyeight.models import FootballCompetition,FootballTeam,FootballMatch
from fivethirtyeight.updater import update_competition,update_matches,update_teams
from test_data import teams_update, match_data_update, competition_update


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
        update_matches(match_data_update)
        matches_count = FootballMatch.objects.all().count()
        matches_updated_count = FootballMatch.objects.filter(status="post").count()
        self.assertEqual(matches_count,matches_updated_count)
        
    def test_update_teams(self):
        r = update_teams(teams_update)
        ids = list(FootballTeam.objects.all().values_list('id').order_by('id'))
        espected_ids = [(i,) for i in range(10,31)] + [(97,),(247,)]
        self.assertTrue(r)
        self.assertEqual(FootballTeam.objects.all().count(),23)
        self.assertEqual(ids,espected_ids)