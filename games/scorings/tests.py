import copy
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Team, Match
from .serializers import TeamSerializer


class TestScoring(TestCase):

    def setUp(self):
        # CREATE TEAMS
        self.team_fantastics = Team.objects.create(name="Fantastics")
        self.team_crazy_ones = Team.objects.create(name="Crazy Ones")
        self.team_rebels = Team.objects.create(name="Rebels")
        self.team_fc_super = Team.objects.create(name="FC Super")
        self.team_misfits = Team.objects.create(name="Misfits")

        # CREATE MATCHES
        self.list_match = [
            {
                "team_a": self.team_crazy_ones,
                "score_a": 3,
                "team_b": self.team_rebels,
                "score_b": 3
             },
            {
                "team_a": self.team_fantastics,
                "score_a": 1,
                "team_b": self.team_fc_super,
                "score_b": 0
            },
            {
                "team_a": self.team_crazy_ones,
                "score_a": 1,
                "team_b": self.team_fc_super,
                "score_b": 1
            },
            {
                "team_a": self.team_fantastics,
                "score_a": 3,
                "team_b": self.team_rebels,
                "score_b": 1
            },
            {
                "team_a": self.team_crazy_ones,
                "score_a": 4,
                "team_b": self.team_rebels,
                "score_b": 0
            }
        ]
        for match in self.list_match:
            new_match = Match.objects.create(**match)

    def test_team_models(self):
        team_count = Team.objects.count()
        self.assertEqual(team_count, 5)
        match_count = Match.objects.count()
        self.assertEqual(match_count, 5)
        list_team = Team.objects.all().values_list('name', flat=True)
        self.assertEqual(list_team[0], "Fantastics")
        self.assertEqual(list_team[1], "Crazy Ones")
        self.assertEqual(list_team[2], "FC Super")
        self.assertEqual(list_team[3], "Rebels")
        self.assertEqual(list_team[4], "Misfits")

    def test_total_points(self):
        self.assertEqual(self.team_fantastics.get_total_points(self.team_fantastics.id), 6)
        self.assertEqual(self.team_crazy_ones.get_total_points(self.team_crazy_ones.id), 5)
        self.assertEqual(self.team_fc_super.get_total_points(self.team_fc_super.id), 1)
        self.assertEqual(self.team_rebels.get_total_points(self.team_rebels.id), 1)
        self.assertEqual(self.team_misfits.get_total_points(self.team_misfits.id), 0)

    def test_add_new_match(self):
        new_match_score = {
            "team_a": self.team_misfits,
            "score_a": 2,
            "team_b": self.team_rebels,
            "score_b": 0
        }
        new_match = Match.objects.create(**new_match_score)
        list_team = Team.objects.all().values_list('name', flat=True)
        self.assertEqual(list_team[0], "Fantastics")
        self.assertEqual(list_team[1], "Crazy Ones")
        self.assertEqual(list_team[2], "Misfits")
        self.assertEqual(list_team[3], "FC Super")
        self.assertEqual(list_team[4], "Rebels")


class TestScoringAPI(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_bulk_upload_match(self):
        URL = reverse('scoring:match-upload-file')
        with open('match2.csv') as fp:
            res = self.client.post(URL, {'file': fp})
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Team.objects.all().count(), 5)
        self.assertEqual(Match.objects.all().count(), 5)

        URL_TEAM_LIST = reverse('scoring:team-list')
        res = self.client.get(URL_TEAM_LIST)
        team_serializer = TeamSerializer(Team.objects.all(), many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(team_serializer.data, res.data)







