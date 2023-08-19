from django.contrib import admin
from .models import (
    Competition,Scorers,Standings,Match
)
# Register your models here.

admin.site.register(Competition)
admin.site.register(Match)
admin.site.register(Standings)
admin.site.register(Scorers)
