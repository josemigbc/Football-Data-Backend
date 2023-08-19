from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here

class Competition(models.Model):
    slug = models.SlugField(_("Slug"),unique=True)
    data = models.JSONField(_("Data"))

    class Meta:
        verbose_name = 'Competition'
        verbose_name_plural = 'Competitions'

    def __str__(self):
        return self.data.get('name')

class Match(models.Model):
    
    id = models.IntegerField(_("Id"))
    competition = models.CharField(_("Competition"), max_length=5)
    home_team_id = models.IntegerField(_("Home Team Id"))
    away_team_id = models.IntegerField(_("Away Team Id"))
    datetime = models.DateTimeField(_("Date Time"))
    data = models.JSONField(_("Data"))

    class Meta:
        verbose_name = 'Match'
        verbose_name_plural = 'Matches'

    def __str__(self):
        return f"Match {self.id}"

class Standings(models.Model):
    
    competition = models.CharField(_("Competition"), max_length=5)
    data = models.JSONField(_("Data"))

    class Meta:
        verbose_name = 'Standings'
        verbose_name_plural = 'Standings'

    def __str__(self):
        return f"Standings {self.competition}"

class Scorers(models.Model):
    
    competition = models.CharField(_("Competition"), max_length=5)
    data = models.JSONField(_("Data"))

    class Meta:
        verbose_name = 'Scorers'
        verbose_name_plural = 'Scorers'

    def __str__(self):
        return f"Scorers {self.competition}"