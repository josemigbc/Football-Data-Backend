from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>/", views.MatchRetrieveView.as_view(), name="match"),
    path("competition/<int:pk>/",views.MatchCompetitionListView.as_view(),name="match_competion"),
    path("team/<int:pk>/",views.MatchTeamListView.as_view(), name="match_team"),
    path("date/<int:year>/<int:month>/<int:day>/", views.MatchDateListView.as_view(), name="match_date"),
]