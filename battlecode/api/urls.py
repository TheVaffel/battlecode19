"""
Public endpoints.
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('user/profile', views.UserProfileViewSet, base_name='userprofile')
router.register('user', views.UserViewSet, base_name='user')
router.register('league', views.LeagueViewSet, base_name='league')
router.register('(?P<league_id>[^/.]+)/team', views.TeamViewSet, base_name='team')
router.register('(?P<league_id>[^/.]+)/submission', views.SubmissionViewSet, base_name='submission')
router.register('(?P<league_id>[^/.]+)/scrimmage', views.ScrimmageViewSet, base_name='scrimmage')
router.register('(?P<league_id>[^/.]+)/map', views.MapViewSet, base_name='map')
router.register('(?P<league_id>[^/.]+)/tournament', views.TournamentViewSet, base_name='tournament')

urlpatterns = router.urls
