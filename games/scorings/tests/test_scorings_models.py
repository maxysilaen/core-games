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







