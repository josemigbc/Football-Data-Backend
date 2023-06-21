from django.contrib import admin
from .models import Match,Team,Competition,FTETeam

# Register your models here.
admin.site.register(Match)
admin.site.register(Team)
admin.site.register(Competition)
admin.site.register(FTETeam)
