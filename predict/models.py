from django.db import models
from accounts.models import User
from data.models import Match

# Create your models here.
class Game(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    match = models.ForeignKey(Match,on_delete=models.CASCADE)
    amount = models.IntegerField()
    winner = models.CharField(max_length=100,choices=[('1','HOME_TEAM'),('X','DRAW'),('2','AWAY_TEAM')])
    odds_HOME = models.FloatField()
    odds_DRAW = models.FloatField()
    odds_AWAY = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
class Odds(models.Model):
    
    match = models.ForeignKey(Match,on_delete=models.CASCADE)
    odds_HOME = models.FloatField()
    odds_DRAW = models.FloatField()
    odds_AWAY = models.FloatField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)