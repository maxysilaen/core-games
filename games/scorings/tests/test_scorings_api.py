from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from model_mommy import mommy

from scorings.models import Team, Match
from scorings.serializers import TeamSerializer, MatchSerializer


def detail_match_url(match_id):
    return reverse('scoring:match-detail', args=[match_id])


def is_descending(val):
    # Funct check the val is descending
   for a in range(1, len(val)):
      if val[a] > val[a-1]:
         return False
      return True


class TestScoringAPI(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = mommy.make(get_user_model())
        self.client.force_authenticate(self.user)

    def test_bulk_upload_match(self):
        URL = reverse('scoring:match-upload-file')
        with open('match2.csv') as fp:
            res = self.client.post(URL, {'file': fp})
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        URL_TEAM_LIST = reverse('scoring:team-list')
        res = self.client.get(URL_TEAM_LIST)
        team_serializer = TeamSerializer(Team.objects.all(), many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(team_serializer.data, res.data)

        # Check if the data is ordered correctly
        res_data = res.data
        points = []
        [points.append(data["total_points"]) for data in res_data]
        self.assertTrue(bool(is_descending(points)))

        URL_MATCH_LIST = reverse('scoring:match-list')
        res = self.client.get(URL_MATCH_LIST)
        match_serializer = MatchSerializer(Match.objects.all(), many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(match_serializer.data, res.data)

    def test_update_match(self):
        self.match_1 = mommy.make(Match)
        url = detail_match_url(self.match_1.match_id)
        payload = {
            "score_a": 10,
        }
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.match_1.refresh_from_db()
        self.assertEqual(self.match_1.score_a, payload['score_a'])



