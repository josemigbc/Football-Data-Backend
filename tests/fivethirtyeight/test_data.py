import json
from django.conf import settings

manage_teams_expected_data = [
            {
                "rank": "1",
                '': '',
                'name': 'Man. City',
                'national_league': 1,
                'country': "England",
                'offensive': "2.8",
                'defensive': "0.3",
                'spi': "92.0",
                "id": 382,
                "logo": "https://secure.espn.com/combiner/i?img=/i/teamlogos/soccer/500/382.png&w=56",
            },
            {
                "rank": "2",
                '': "",
                'name': "Bayern Munich",
                'national_league': 1,
                'country': "Germany",
                'offensive': "3.0",
                'defensive': "0.7",
                'spi': "87.7",
                "id": 132,
                "logo":"https://secure.espn.com/combiner/i?img=/i/teamlogos/soccer/500/132.png&w=56",
            }
        ]

manage_competition_expected_data = {
    "name": "Serie A",
    "country": "Italia",
    "season": "2022",
    "last_updated": "Actualizado 27 de Mayo de 2023 16:41",
    "logo": "https://projects.fivethirtyeight.com/soccer-predictions/images/serie-a-logo.png?v=13de7574",
}

get_competition_expected_data = {
            "name": "Serie A",
            "country": "Italia",
            "season": "2022",
            "last_updated": "Actualizado 27 de Mayo de 2023 16:41",
            "logo": "https://projects.fivethirtyeight.com/soccer-predictions/images/serie-a-logo.png?v=13de7574",
            "id": 1869,
            "standings": {
                "last_updated":"2023-06-04T21:06:46Z",
                "forecasts":[
                    {
                        "last_updated":"2023-06-04T21:06:46Z",
                        "league_id":1869,
                        "teams":[
                            {"team": 1},
                            {"team": 2},
                        ]
                    }
                ]
            },
            "name_url": "test",
            "last_updated": "2023-06-04T21:06:46Z"
        }

get_matches_expected_data = [
            {
                "id":401454164, "league_id":1869,"competition":1869, "datetime":"2022-08-12T19:00:00Z","status":"post",
                "leg":None,"team1":97,"team2":243,"team1_id":97,"team2_id":243,"team1_code":"OSA",
                "team2_code":"SEV","prob1":0.34426,"prob2":0.35899,"probtie":0.29675,"round":None,"matchday":None,
                "score1":2,"score2":1,"adj_score1":2.1,"adj_score2":1.05,"chances1":1.438,"chances2":1.087,
                "moves1":0.7,"moves2":1.122,"aggregate_winner":None,"shootout_winner":None,
            }
        ]

response_matches_data = [
            {
                "id":401454164, "league_id":1869, "datetime":"2022-08-12T19:00:00Z","status":"post",
                "leg":None,"team1":"Osasuna","team2":"Sevilla FC","team1_id":97,"team2_id":243,"team1_code":"OSA",
                "team2_code":"SEV","prob1":0.34426,"prob2":0.35899,"probtie":0.29675,"round":None,"matchday":None,
                "score1":2,"score2":1,"adj_score1":2.1,"adj_score2":1.05,"chances1":1.438,"chances2":1.087,
                "moves1":0.7,"moves2":1.122,"aggregate_winner":None,"shootout_winner":None
            }
        ]

get_standings_expected_data = {
            "last_updated":"2023-06-04T21:06:46Z",
            "forecasts":[
                {
                    "last_updated":"2023-06-04T21:06:46Z",
                    "league_id":1869,
                    "teams":[
                        {"team": 1},
                        {"team": 2},
                    ]
                }
            ]
        }

competition_data_ok = {
    "id": 340,
    "name":"Liga Test",
    "name_url":"/liga-test/",
    "logo":"logo.png",
    "country":"Country",
    "season":"2023",
    "standings":{
        1:{"name": "Test 1"},
        2:{"name": "Test 2"},
    }
}

competition_data_without_name = competition_data_ok.copy()
competition_data_without_name.pop("name")

competition_data_without_name_url = competition_data_ok.copy()
competition_data_without_name_url.pop("name_url")

competition_data_without_country = competition_data_ok.copy()
competition_data_without_country.pop("country")

competition_data_without_id = competition_data_ok.copy()
competition_data_without_id.pop("id")

competition_data_with_another_id = competition_data_ok.copy()
competition_data_with_another_id["id"] = 342

team_data_ok = {
    "id":23,
    "name":"Test Team",
    "logo":"logo.png",
    "rank":3,
    "offensive":3.1,
    "defensive":0.5,
    "spi":90.34,
}

team_data_without_name = team_data_ok.copy()
team_data_without_name.pop("name")

team_data_without_rank = team_data_ok.copy()
team_data_without_rank.pop("rank")

team_data_without_national_league = team_data_ok.copy()

team_data_without_off = team_data_ok.copy()
team_data_without_off.pop("offensive")

team_data_without_spi = team_data_ok.copy()
team_data_without_spi.pop("spi")

team_data_without_id = team_data_ok.copy()
team_data_without_id.pop("id")

team_data_with_another_id = team_data_ok.copy()
team_data_with_another_id["id"] = 24

team_data_ok2 = team_data_ok.copy()
team_data_ok2["id"] = 24
team_data_ok2["name"] = "Test Team 2"

match_data_prematch_ok = {
    "id":23,
    "prob1":0.25,
    "prob2":0.45,
    "probtie":0.3,
}

match_data_postmatch_ok = {
    "id":24,
    "prob1":0.25,
    "prob2":0.45,
    "probtie":0.3,
    "score1":2,
    "score2":1,
}

match_data_without_team1 = match_data_prematch_ok.copy()

match_data_without_team2 = match_data_prematch_ok.copy()

match_data_without_competition = match_data_prematch_ok.copy()

match_data_without_prob1 = match_data_prematch_ok.copy()
match_data_without_prob1.pop('prob1')

match_data_without_prob2 = match_data_prematch_ok.copy()
match_data_without_prob2.pop('prob2')

match_data_without_probtie = match_data_prematch_ok.copy()
match_data_without_probtie.pop('probtie')

match_data_update = [{
    'id': f"{i}",
    'league_id': 243,
    'competition': 243,
    'datetime': f'2022-08-{i-110}T19:00:00Z',
    'status': 'post',
    'leg': None,
    'team1': 97,
    'team2': 247,
    'team1_id': 97,
    'team2_id': 243,
    'team1_code': 'OSA',
    'team2_code': 'SEV',
    'prob1': 0.34426,
    'prob2': 0.35899,
    'probtie': 0.29675,
    'round': None,
    'matchday': None,
    'score1': 2,
    'score2': 1,
    'adj_score1': 2.1,
    'adj_score2': 1.05,
    'chances1': 1.438,
    'chances2': 1.087,
    'moves1': 0.7,
    'moves2': 1.122,
    'aggregate_winner': None,
    'shootout_winner': None
} for i in range(120,140)]

teams_update = [{
    'rank': f'{i-9}',
    '': '',
    'name': f'Man. City {i}',
    'national_league': 243, 
    'country': 'England', 
    'offensive': '2.8',
    'defensive': '0.3', 
    'spi': '92.0',
    'id': i,
    'logo': 'https://secure.espn.com/combiner/i?img=/i/teamlogos/soccer/500/382.png&w=56',
} for i in range(10,31)]

with open(settings.BASE_DIR / "tests/fivethirtyeight/tests_soup/2022_la-liga_forecast_test.json","rb") as file:
    standings = json.load(file)

competition_update = {
    'logo': 'https://projects.fivethirtyeight.com/soccer-predictions/images/la-liga-logo.png?v=16d33bfb',
    'name': 'La Liga',
    'country': 'Spain',
    'season': '2022',
    'last_updated': '2023-06-04T21:06:46Z',
    'id': '1869',
    'name_url': 'la-liga',
    'standings': standings,
}
