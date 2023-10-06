from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MatchViewSet, TeamViewSet
router = DefaultRouter()
router.register('match', MatchViewSet)
router.register('team', TeamViewSet)

app_name = 'scorings'

urlpatterns = [
    path('', include(router.urls))
]
