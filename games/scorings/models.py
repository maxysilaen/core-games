import uuid

from django.db import models
from django.db.models import Q

# Create your models here.
# Models TEAM


class Team(models.Model):

    dict_points = {
        "WIN THE MATCH": 3,
        "LOSE THE MATCH": 0,
        "DRAW THE MATCH": 1
    }

    name = models.CharField(max_length=150, unique=True)
    created_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_date = models.DateField(blank=True, null=True)

    @classmethod
    def total_points(cls):
        list_match = Match.objects.filter((Q(team_a=cls) | Q(team_b=cls)))
        total_points = 0
        for match in list_match:
            result_team_a, result_team_b = match.result_team
            total_points += (cls.dict_points.get(result_team_a) + cls.dict_points.get(result_team_b))
        return total_points

    def __str__(self):
        return self.name


class Match(models.Model):
    match_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    team_a = models.ForeignKey(
        Team,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="team_a_set")
    score_a = models.IntegerField()
    team_b = models.ForeignKey(
        Team,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="team_b_set")
    score_b = models.IntegerField()
    created_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_date = models.DateField(blank=True, null=True)

    @property
    def result_team(self):
        result_team_a, result_team_b = ("DRAW THE MATCH", "DRAW THE MATCH")
        if self.score_a > self.score_b:
            result_team_a, result_team_b = ("WIN THE MATCH", "LOSE THE MATCH")
        elif self.score_a < self.score_b:
            result_team_a, result_team_b = ("LOSE THE MATCH", "WIN THE MATCH")
        elif self.score_a == self.score_b:
            result_team_a, result_team_b = ("DRAW THE MATCH", "DRAW THE MATCH")
        return result_team_a, result_team_b

    def __str__(self):
        return self.match_id