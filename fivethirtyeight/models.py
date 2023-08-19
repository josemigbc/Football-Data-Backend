from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class FootballCompetition(models.Model):
    id = models.PositiveIntegerField(_("Id"),unique=True,primary_key=True)
    name = models.CharField(_("Name"), max_length=50,unique=True)
    name_url = models.CharField(_("URL"), max_length=200)
    logo = models.URLField(_("Logo"), max_length=200,null=True,blank=True)
    country = models.CharField(_("Country"), max_length=50)
    season = models.CharField(_("Season"), max_length=10)
    last_updated = models.DateTimeField(_("Last Updated"), auto_now=True, auto_now_add=False)
    standings = models.JSONField(_("Standings"),null=True,blank=True)
    
    class Meta:
        verbose_name = _("Football Competition")
        verbose_name_plural = _("Football Competions")

    def __str__(self):
        return self.name
    
class FootballTeam(models.Model):
    id = models.PositiveIntegerField(_("Id"),unique=True,primary_key=True)
    name = models.CharField(_("Name"), max_length=50,unique=True)
    rank = models.PositiveIntegerField(_("Rank"))
    national_league = models.ForeignKey(FootballCompetition, verbose_name=_("Competition"), on_delete=models.CASCADE)
    offensive = models.DecimalField(_("Offensive"),decimal_places=2,max_digits=4)
    defensive = models.DecimalField(_("Defensive"),decimal_places=2,max_digits=4)
    spi = models.DecimalField(_("SPI"),decimal_places=2,max_digits=4)
    logo = models.URLField(_("Logo"), max_length=200,null=True,blank=True)

    class Meta:
        verbose_name = _("Football Team")
        verbose_name_plural = _("Football Teams")

    def __str__(self):
        return self.name
    
class FootballMatch(models.Model):
    id = models.PositiveIntegerField(_("Id"),unique=True,primary_key=True)
    team1 = models.ForeignKey(FootballTeam,verbose_name=_("Home Team"), on_delete=models.CASCADE,related_name="home_team")
    team2 = models.ForeignKey(FootballTeam, verbose_name=_("Away Team"), on_delete=models.CASCADE,related_name="away_team")
    score1 = models.PositiveIntegerField(_("Fulltime Home"),null=True,blank=True)
    score2 = models.PositiveIntegerField(_("Fulltime Away"),null=True,blank=True)
    competition = models.ForeignKey(FootballCompetition, verbose_name=_("Competition"), on_delete=models.CASCADE)
    datetime = models.DateTimeField(_("DateTime"))
    prob1 = models.DecimalField(_("Prob Home"),decimal_places=5,max_digits=6)
    prob2 = models.DecimalField(_("Prob Away"),decimal_places=5,max_digits=6)
    probtie = models.DecimalField(_("Prob Draw"),decimal_places=5,max_digits=6)
    round = models.CharField(_("Round"), max_length=1,null=True,blank=True)
    matchday = models.PositiveIntegerField(_("Matchday"),null=True,blank=True)
    group = models.CharField(_("Group"), max_length=1,null=True,blank=True)
    leg = models.PositiveIntegerField(_("Leg"),null=True,blank=True)
    status = models.CharField(_("Status"), max_length=5,null=True,blank=True)
    
    class Meta:
        verbose_name = _("Match")
        verbose_name_plural = _("Matches")

    def __str__(self):
        return f"{self.team1} vs {self.team2}"
