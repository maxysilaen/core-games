from rest_framework import serializers

from .models import (
   Team, Match
)


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name', 'total_points')
        read_only_fields = 'total_points',


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'
        read_only_fields = 'match_id',


class MatchUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ('file',)