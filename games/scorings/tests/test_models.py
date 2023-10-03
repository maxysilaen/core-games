from django.test import TestCase

from scorings.models import Team, Match


class TestScoring(TestCase):

    def setUp(self):
        # CREATE TEAMS
        self.team_fantastics = Team.objects.create(name="Fantastics")
        self.team_crazy_ones = Team.objects.create(name="Crazy Ones")
        self.team_rebels = Team.objects.create(name="Rebels")
        self.team_fc_super = Team.objects.create(name="FC Super")
        self.team_misfits = Team.objects.create(name="Misfits")

        # CREATE MATCHES
        list_match = [
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
        for match in list_match:
            new_match = Match.objects.create(**match)

    def test_team_models(self):
        team_count = Team.objects.count()
        self.assertEqual(team_count, 5)
        match_count = Match.objects.count()
        self.assertEqual(match_count, 5)





