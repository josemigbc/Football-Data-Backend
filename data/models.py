from django.db import models

# Create your models here.

class Competition(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    logo = models.TextField()

class FTETeam(models.Model):
    name = models.CharField(max_length=100,unique=True)
class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100,unique=True)
    short_name = models.CharField(max_length=50,unique=True)
    tla = models.CharField(max_length=3,unique=True)
    fte_name = models.OneToOneField(FTETeam,on_delete=models.CASCADE,null=True,blank=True)
    logo = models.TextField()

class Match(models.Model):
    id = models.IntegerField(primary_key=True)
    competition = models.ForeignKey(Competition,on_delete=models.CASCADE)
    utcDate = models.DateTimeField()
    status = models.CharField(max_length=100,choices=[("SCHEDULED","SCHEDULED"),("FINISHED","FINISHED"),("TIMED","TIMED"),("LIVE","LIVE"),("IN_PLAY","IN_PLAY"),("POSTPONED","POSTPONED"),("SUSPENDED","SUSPENDED"),("CANCELLED","CANCELLED")])
    matchday = models.IntegerField()
    stage = models.CharField(max_length=100)
    group = models.CharField(max_length=100,null=True,blank=True)
    last_updated = models.DateTimeField()
    winner = models.CharField(max_length=100,choices=[('HOME_TEAM','HOME_TEAM'),('DRAW','DRAW'),('AWAY_TEAM','AWAY_TEAM')],null=True,blank=True)
    duration = models.CharField(max_length=100,choices=[("REGULAR","REGULAR"),( "EXTRA_TIME", "EXTRA_TIME"),("PENALTY_SHOOTOUT","PENALTY_SHOOTOUT")])
    fulltime_home = models.IntegerField(null=True,blank=True)
    fulltime_away = models.IntegerField(null=True,blank=True)
    halftime_home = models.IntegerField(null=True,blank=True)
    halftime_away = models.IntegerField(null=True,blank=True)
    referee = models.TextField(null=True,blank=True)
    home_team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name="home_team")
    away_team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name="away_team")