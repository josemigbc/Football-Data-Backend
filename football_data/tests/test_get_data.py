from django.test import TestCase
from unittest.mock import patch, Mock
import requests
import datetime
from football_data.data import Data
from football_data.models import Competition, Match, Scorers, Standings


class DataTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.data_getter = Data()
        cls.data = {"data": "Test data"}

    @patch("requests.get")
    def test_do_get_with_ok(self, mock_get: Mock):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = self.data

        result = self.data_getter.do_get("LT")
        self.assertEqual(result, self.data)

    @patch("requests.get")
    def test_do_get_with_fail(self, mock_get: Mock):
        mock_response = mock_get.return_value
        mock_response.status_code = 400

        with self.assertRaises(requests.exceptions.RequestException):
            self.data_getter.do_get("LT")

    @patch.object(Data, 'do_get')
    def test_get_competition_doesnot_exist_response_ok(self, mock_get: Mock):
        mock_get.return_value = self.data
        r = self.data_getter.get_competition("LT")
        mock_get.assert_called_once_with("LT")
        competition = Competition.objects.get(slug="LT")
        self.assertEqual(competition.data, self.data)
        self.assertEqual(r, (True, "created"))

    @patch.object(Data, 'do_get')
    def test_get_competition_doesnot_exist_response_fail(self, mock_get: Mock):
        mock_get.return_value = {}
        with self.assertRaises(ValueError):
            self.data_getter.get_competition("LT")
        mock_get.assert_called_once_with("LT")

    def test_get_competition_does_exist_response_ok(self):
        Competition.objects.create(slug="LT", data=self.data)
        r = self.data_getter.get_competition("LT")
        self.assertEqual(r, (False, "already exists"))

    @patch.object(Data, 'do_get')
    def test_get_match_with_match_doesnot_exist_response_ok(self, mock_get: Mock):
        mock_get.return_value = {
            "matches": [
                {
                    "id": 1000,
                    "utcDate": "2023-08-11T15:00",
                    "homeTeam": {
                        "id": 1,
                    },
                    "awayTeam": {
                        "id": 2,
                    }
                },
            ]
        }

        self.data_getter.get_matches("LT")
        match = Match.objects.get(id=1000)
        self.assertEqual(match.home_team_id, 1)

    @patch.object(Data, 'do_get')
    def test_get_match_with_match_does_exist_response_ok(self, mock_get: Mock):

        Match.objects.create(
            id=1000,
            datetime=datetime.datetime(2023, 8, 11, 15, 0),
            home_team_id=1,
            away_team_id=2,
            data=self.data,
        )

        match_data = {
            "id": 1000,
            "utcDate": "2023-08-11T20:00",
            "homeTeam": {
                "id": 1,
            },
            "awayTeam": {
                "id": 2,
            }
        },

        mock_get.return_value = {
            "matches": [
                match_data[0],
            ]
        }

        self.data_getter.get_matches("LT")
        match = Match.objects.get(id=1000)

        mock_get.assert_called_once_with("LT/matches")
        self.assertEqual(match.datetime.time(),
                         datetime.datetime(2023, 8, 11, 20, 0).time())
        self.assertEqual(match.data, match_data[0])

    @patch.object(Data, 'do_get')
    def test_get_match_with_response_fail(self, mock_get: Mock):
        mock_get.return_value = {}
        with self.assertRaises(ValueError):
            self.data_getter.get_matches("LT")
        mock_get.assert_called_once_with("LT/matches")

    @patch.object(Data, 'do_get')
    def test_get_standings_doesnot_exist_response_ok(self, mock_get: Mock):
        mock_get.return_value = {
            "standings": [
                self.data,
            ]
        }

        r = self.data_getter.get_standings("LT")
        mock_get.assert_called_once_with("LT/standings")
        standings = Standings.objects.get(competition="LT")
        self.assertEqual(standings.data, [self.data])
        self.assertEqual(r, (True, "created"))

    @patch.object(Data, 'do_get')
    def test_get_standings_doesnot_exist_response_fail(self, mock_get: Mock):
        mock_get.return_value = {}
        with self.assertRaises(ValueError):
            self.data_getter.get_standings("LT")
        mock_get.assert_called_once_with("LT/standings")

    @patch.object(Data, 'do_get')
    def test_get_standings_does_exist_response_ok(self, mock_get: Mock):
        Standings.objects.create(competition="LT", data=self.data)

        mock_get.return_value = {
            "standings": [
                self.data,
            ]
        }

        r = self.data_getter.get_standings("LT")
        standings = Standings.objects.get(competition="LT")
        self.assertEqual(r, (True, "updated"))
        self.assertEqual(standings.data, [self.data])

    @patch.object(Data, 'do_get')
    def test_get_scorers_doesnot_exist_response_ok(self, mock_get: Mock):
        mock_get.return_value = {
            "scorers": [
                self.data,
            ]
        }

        r = self.data_getter.get_scorers("LT")
        mock_get.assert_called_once_with("LT/scorers")
        scorers = Scorers.objects.get(competition="LT")
        self.assertEqual(scorers.data, [self.data])
        self.assertEqual(r, (True, "created"))

    @patch.object(Data, 'do_get')
    def test_get_scorers_doesnot_exist_response_fail(self, mock_get: Mock):
        mock_get.return_value = {}
        with self.assertRaises(ValueError):
            self.data_getter.get_scorers("LT")
        mock_get.assert_called_once_with("LT/scorers")

    @patch.object(Data, 'do_get')
    def test_get_scorers_does_exist_response_ok(self, mock_get: Mock):
        Scorers.objects.create(competition="LT", data=self.data)

        mock_get.return_value = {
            "scorers": [
                self.data,
            ]
        }

        r = self.data_getter.get_scorers("LT")
        scorers = Scorers.objects.get(competition="LT")
        self.assertEqual(r, (True, "updated"))
        self.assertEqual(scorers.data, [self.data])
