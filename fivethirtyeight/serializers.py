from rest_framework import serializers
from .models import FootballTeam,FootballCompetition,FootballMatch
from django.forms import ModelForm
        
class FootballCompetitionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FootballCompetition
        fields = '__all__'
        
class FootballCompetitionForMatchAndTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = FootballCompetition
        exclude = ('standings',)

class FootballTeamSerializer(serializers.ModelSerializer):
    
    national_league = FootballCompetitionForMatchAndTeamSerializer(read_only=True,many=False)
    
    class Meta:
        model = FootballTeam
        fields = '__all__'
        
class FootballTeamNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FootballTeam
        fields = ('id','name','logo')

class FootballMatchSerializer(serializers.ModelSerializer):
    
    competition = FootballCompetitionForMatchAndTeamSerializer(read_only=True,many=False)
    team1 = FootballTeamSerializer(read_only=True,many=False)
    team2 = FootballTeamSerializer(read_only=True,many=False)
    class Meta:
        model = FootballMatch
        fields = '__all__'
        
class FootballTeamForm(ModelForm):
    class Meta:
        model = FootballTeam
        fields = '__all__'
        
class FootballMatchForm(ModelForm):
    class Meta:
        model = FootballMatch
        fields = '__all__'