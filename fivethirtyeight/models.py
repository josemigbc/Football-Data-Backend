from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.serializers.json import DjangoJSONEncoder,Deserializer

# Create your models here.
class FootballCompetition(models.Model):
    id = models.PositiveIntegerField(_("Id"),unique=True,primary_key=True)
    name = models.CharField(_("name"), max_length=50,unique=True)
    name_url = models.CharField(_("name_url"), max_length=200)
    logo = models.URLField(_("url"), max_length=200,null=True,blank=True)
    country = models.CharField(_("country"), max_length=50)
    season = models.CharField(_("season"), max_length=10)
    last_updated = models.DateTimeField(_("Last Updated"), auto_now=True, auto_now_add=False)
    standings = models.JSONField(_("standings"),null=True,blank=True)
    
    class Meta:
        verbose_name = _("Football Competition")
        verbose_name_plural = _("Football Competions")

    def __str__(self):
        return self.name
    
class FootballTeam(models.Model):
    id = models.PositiveIntegerField(_("Id"),unique=True,primary_key=True)
    name = models.CharField(_("name"), max_length=50,unique=True)
    rank = models.PositiveIntegerField(_("rank"))
    national_league = models.ForeignKey(FootballCompetition, verbose_name=_("Competition"), on_delete=models.CASCADE)
    offensive = models.DecimalField(_("offensive"),decimal_places=2,max_digits=4)
    defensive = models.DecimalField(_("defensive"),decimal_places=2,max_digits=4)
    spi = models.DecimalField(_("spi"),decimal_places=2,max_digits=4)
    logo = models.URLField(_("url"), max_length=200,null=True,blank=True)

    class Meta:
        verbose_name = _("Football Team")
        verbose_name_plural = _("Football Teams")

    def __str__(self):
        return self.name
    
class FootballMatch(models.Model):
    id = models.PositiveIntegerField(_("Id"),unique=True,primary_key=True)
    team1 = models.ForeignKey(FootballTeam, on_delete=models.CASCADE,related_name="home_team")
    team2 = models.ForeignKey(FootballTeam, on_delete=models.CASCADE,related_name="away_team")
    score1 = models.PositiveIntegerField(_("fulltime_home"),null=True,blank=True)
    score2 = models.PositiveIntegerField(_("fulltime_away"),null=True,blank=True)
    competition = models.ForeignKey(FootballCompetition, verbose_name=_("competition"), on_delete=models.CASCADE)
    datetime = models.DateTimeField(_("datetime"))
    prob1 = models.DecimalField(_("prob_home"),decimal_places=5,max_digits=6)
    prob2 = models.DecimalField(_("prob_away"),decimal_places=5,max_digits=6)
    probtie = models.DecimalField(_("prob_draw"),decimal_places=5,max_digits=6)
    round = models.CharField(_("round"), max_length=1,null=True,blank=True)
    matchday = models.PositiveIntegerField(_("matchday"),null=True,blank=True)
    group = models.CharField(_("group"), max_length=1,null=True,blank=True)
    leg = models.PositiveIntegerField(_("matchday"),null=True,blank=True)
    status = models.CharField(_("status"), max_length=5,null=True,blank=True)
    
    class Meta:
        verbose_name = _("Match")
        verbose_name_plural = _("Matches")

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"
