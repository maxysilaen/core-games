import csv
import io
from rest_framework import (
    viewsets,
    status
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Team, Match
from .serializers import (TeamSerializer,
                          MatchSerializer,
                          MatchUploadSerializer)

# Create your views here.


class TeamViewSet(viewsets.ModelViewSet):
    """Base viewset for recipe attributes"""
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class MatchViewSet(viewsets.ModelViewSet):
    """Base viewset for recipe attributes"""
    serializer_class = MatchSerializer
    queryset = Match.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'bulk_create_match':
            return MatchUploadSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def _get_or_create_team(self, name_team):
        instance, created = Team.objects.get_or_create(name=name_team)
        return instance

    @action(['POST'], detail=False, url_name='upload-file')
    def bulk_create_match(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        decoded_file = file.read().decode()
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string)
        for row in reader:
            dict_match = {
                "team_a": self._get_or_create_team(row[0]),
                "score_a": row[1],
                "team_b": self._get_or_create_team(row[2]),
                "score_b": row[3]
            }
            new_match = Match.objects.create(**dict_match)
        return Response(status=status.HTTP_204_NO_CONTENT)
