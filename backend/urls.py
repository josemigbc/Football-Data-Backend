"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from accounts.views import UserView
from balance.views import BalanceView
from data.views import TeamRetrieve,CompetitionRetrieve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/user/", UserView.as_view(), name="user"),
    path("api/balance/",BalanceView.as_view(),name="balance"),
    path("api/team/<int:pk>/", TeamRetrieve.as_view(), name="team"),
    path("api/competition/<int:pk>/", CompetitionRetrieve.as_view(), name=""),
    path("api/match/",include("data.urls")),
]