from django.contrib import admin
from .models import FootballCompetition,FootballMatch,FootballTeam

# Register your models here.

admin.site.register(FootballTeam)
admin.site.register(FootballCompetition)
admin.site.register(FootballMatch)
