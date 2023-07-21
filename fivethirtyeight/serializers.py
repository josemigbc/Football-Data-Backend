from rest_framework import serializers
from .models import FootballTeam,FootballCompetition,FootballMatch

class FootballTeamSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FootballTeam
        fields = '__all__' 
        
class FootballCompetitionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FootballCompetition
        fields = '__all__'
        
                
class FootballMatchSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FootballMatch
        fields = '__all__'