from rest_framework import serializers
from .models import Match,Competition,Team,FTETeam

class FTETeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = FTETeam
        fields = '__all__'
        
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        
class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = '__all__'
        
class MatchSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer(read_only=True)
    away_team = TeamSerializer(read_only=True)
    competition = CompetitionSerializer(read_only=True)
    class Meta:
        model = Match
        fields = '__all__'
        depth = 1