import uuid

from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
# Models TEAM

class TeamQuerySet(models.QuerySet):
    def all(self):
        return self.order_by('-total_points', 'name')


class TeamManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return TeamQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()


class Team(models.Model):

    dict_points = {
        "WIN THE MATCH": 3,
        "LOSE THE MATCH": 0,
        "DRAW THE MATCH": 1
    }
    name = models.CharField(max_length=150, unique=True)
    total_points = models.IntegerField(default=0)
    created_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_date = models.DateField(blank=True, null=True)
    objects = TeamManager()

    @classmethod
    def get_total_points(cls, id):
        total_points = 0
        point_a = 0
        point_b = 0
        team = cls.objects.get(id=id)
        list_matches = Match.objects.filter((Q(team_a=team) | Q(team_b=team)))
        for match in list_matches:
            result_team_a, result_team_b = match.result_team
            if match.team_a == team:
                point_a = cls.dict_points.get(result_team_a)
            elif match.team_b == team:
                point_b = cls.dict_points.get(result_team_b)
            total_points += (point_a + point_b)
        return total_points

    def __str__(self):
        return self.name


class Match(models.Model):
    """
        in this case one match only two teams
    """

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
        if self.score_a > self.score_b:
            result_team_a, result_team_b = ("WIN THE MATCH", "LOSE THE MATCH")
        elif self.score_a < self.score_b:
            result_team_a, result_team_b = ("LOSE THE MATCH", "WIN THE MATCH")
        elif self.score_a == self.score_b:
            result_team_a, result_team_b = ("DRAW THE MATCH", "DRAW THE MATCH")
        return result_team_a, result_team_b

    def __str__(self):
        return self.match_id


@receiver(post_save, sender=Match)
def create_match(sender, created, instance, **kwargs):
    # Update Team A and Team B points
    point_a = instance.team_a.get_total_points(instance.team_a.id)
    point_b = instance.team_b.get_total_points(instance.team_b.id)

    instance.team_a.total_points = point_a
    instance.team_a.save()
    instance.team_b.total_points = point_b
    instance.team_b.save()
    return instance

