from django.db import models

# Create your models here.

class Competition(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    logo = models.TextField()

class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    tla = models.CharField(max_length=3)
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
    winner = models.CharField(max_length=100,choices=[('1','HOME_TEAM'),('X','DRAW'),('2','AWAY_TEAM')])
    duration = models.CharField(max_length=100,choices=[("REGULAR","REGULAR"),( "EXTRA_TIME", "EXTRA_TIME"),("PENALTY_SHOOTOUT","PENALTY_SHOOTOUT")])
    fulltime_home = models.IntegerField()
    fulltime_away = models.IntegerField()
    halftime_home = models.IntegerField()
    halftime_away = models.IntegerField()
    referee = models.TextField()
    home_team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name="home_team")
    away_team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name="away_team")