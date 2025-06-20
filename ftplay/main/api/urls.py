from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views.auth import RegisterView, LoginView, ChangePasswordView
from .views.player import PlayerProfileView, PlayerRankScoreView
from .views.organizer import OrganizerProfileView
from .views.game import GameViewSet

router = DefaultRouter()
router.register(r'games', GameViewSet, basename='game')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('player/profile/', PlayerProfileView.as_view(), name='player_profile'),
    path('player/rank-scores/', PlayerRankScoreView.as_view(), name='player_rank_scores'),
    path('organizer/profile/', OrganizerProfileView.as_view(), name='organizer_profile'),
    path('', include(router.urls)),
] 