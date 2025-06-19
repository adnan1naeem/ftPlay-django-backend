from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import auth, game
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views.auth import ChangePasswordView, RegisterView, LoginView
from .views.player import PlayerProfileView, PlayerRankScoreView

router = DefaultRouter()
router.register(r'games', game.GameViewSet)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/change-password/', auth.ChangePasswordView.as_view(), name='change_password'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('player/profile/', PlayerProfileView.as_view(), name='player_profile'),
    path('player/rank-scores/', PlayerRankScoreView.as_view(), name='player_rank_scores'),
    path('', include(router.urls)),
] 