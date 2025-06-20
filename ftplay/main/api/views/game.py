from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from ..serializers.game import (
    GameSerializer, 
    GameCreateSerializer, 
    GameUpdateSerializer,
    GameRatingSerializer, 
    GameCommentSerializer
)
from main.models import Game, GameRating, GameComment, Organizer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return GameCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return GameUpdateSerializer
        return GameSerializer

    def get_queryset(self):
        """Filter games based on user role and permissions, and update statuses"""
        user = self.request.user
        
        # Update game statuses before returning queryset
        Game.update_all_game_statuses()
        
        # If user is an organizer, show their games
        if hasattr(user, 'organizer'):
            return Game.objects.filter(organizer=user.organizer)
        
        # If user is a player, show games they can participate in
        elif hasattr(user, 'player'):
            return Game.objects.filter(visibility='PUBLIC')
        
        return Game.objects.none()

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single game and update its status"""
        instance = self.get_object()
        # Update the game status before returning
        instance.update_status()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """Create a game and assign the current organizer as the creator"""
        user = self.request.user
        
        # Check if user is an organizer
        if not hasattr(user, 'organizer'):
            raise PermissionDenied("Only organizers can create games")
        
        serializer.save(organizer=user.organizer)

    def perform_update(self, serializer):
        """Update a game - only the creator can update"""
        game = self.get_object()
        user = self.request.user
        
        # Check if user is the organizer who created this game
        if not hasattr(user, 'organizer') or game.organizer != user.organizer:
            raise PermissionDenied("Only the game creator can update this game")
        
        # Prevent updating if game is already completed or canceled
        if game.status in ['COMPLETED', 'CANCELED']:
            raise PermissionDenied("Cannot update a completed or canceled game")
        
        serializer.save()

    def perform_destroy(self, instance):
        """Prevent deletion - use cancel instead"""
        raise PermissionDenied("Games cannot be deleted. Use cancel instead.")

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a game - only the creator can cancel"""
        game = self.get_object()
        user = self.request.user
        
        # Check if user is the organizer who created this game
        if not hasattr(user, 'organizer') or game.organizer != user.organizer:
            raise PermissionDenied("Only the game creator can cancel this game")
        
        # Check if game can be canceled
        if game.status in ['COMPLETED', 'CANCELED']:
            return Response(
                {'error': 'Game is already completed or canceled'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cancel the game
        game.status = 'CANCELED'
        game.save()
        
        return Response(
            {'message': 'Game canceled successfully', 'status': game.status},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a game as a player"""
        game = self.get_object()
        user = self.request.user
        
        # Check if user is a player
        if not hasattr(user, 'player'):
            raise PermissionDenied("Only players can join games")
        
        # Update game status before checking
        game.update_status()
        
        # Check if game is joinable
        if game.status != 'UPCOMING':
            return Response(
                {'error': 'Game is not open for joining'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if player is already in the game
        if game.participants.filter(id=user.player.id).exists():
            return Response(
                {'error': 'Already joined this game'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if game is full
        if game.participants.count() >= game.number_of_participants:
            return Response(
                {'error': 'Game is full'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Join the game
        game.participants.add(user.player)
        
        return Response(
            {'message': 'Successfully joined the game'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a game as a player"""
        game = self.get_object()
        user = self.request.user
        
        # Check if user is a player
        if not hasattr(user, 'player'):
            raise PermissionDenied("Only players can leave games")
        
        # Check if player is in the game
        if not game.participants.filter(id=user.player.id).exists():
            return Response(
                {'error': 'Not joined this game'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Leave the game
        game.participants.remove(user.player)
        
        return Response(
            {'message': 'Successfully left the game'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        """Rate a game"""
        game = self.get_object()
        
        # Update game status before allowing rating
        game.update_status()
        
        # Only allow rating completed games
        if game.status != 'COMPLETED':
            return Response(
                {'error': 'Can only rate completed games'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = GameRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(game=game, player=request.user.player)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        """Comment on a game"""
        game = self.get_object()
        serializer = GameCommentSerializer(data=request.data)
        if serializer.is_valid():
            # Set the appropriate user (player or organizer)
            if hasattr(request.user, 'player'):
                serializer.save(game=game, player=request.user.player)
            elif hasattr(request.user, 'organizer'):
                serializer.save(game=game, organizer=request.user.organizer)
            else:
                raise PermissionDenied("Invalid user type")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def my_games(self, request):
        """Get games created by the current organizer"""
        user = self.request.user
        
        if not hasattr(user, 'organizer'):
            raise PermissionDenied("Only organizers can access this endpoint")
        
        # Update all game statuses before returning
        Game.update_all_game_statuses()
        
        games = Game.objects.filter(organizer=user.organizer)
        serializer = self.get_serializer(games, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def available_games(self, request):
        """Get games available for joining (for players)"""
        user = self.request.user
        
        if not hasattr(user, 'player'):
            raise PermissionDenied("Only players can access this endpoint")
        
        # Update all game statuses before returning
        Game.update_all_game_statuses()
        
        games = Game.objects.filter(
            status='UPCOMING',
            visibility='PUBLIC'
        ).exclude(participants=user.player)
        
        serializer = self.get_serializer(games, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def joined_games(self, request):
        """Get games joined by the current player"""
        user = self.request.user
        
        if not hasattr(user, 'player'):
            raise PermissionDenied("Only players can access this endpoint")
        
        # Update all game statuses before returning
        Game.update_all_game_statuses()
        
        games = Game.objects.filter(participants=user.player)
        serializer = self.get_serializer(games, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def completed_games(self, request):
        """Get completed games for the current user"""
        user = self.request.user
        
        # Update all game statuses before returning
        Game.update_all_game_statuses()
        
        if hasattr(user, 'organizer'):
            # For organizers, show their completed games
            games = Game.objects.filter(organizer=user.organizer, status='COMPLETED')
        elif hasattr(user, 'player'):
            # For players, show completed games they participated in
            games = Game.objects.filter(participants=user.player, status='COMPLETED')
        else:
            games = Game.objects.none()
        
        serializer = self.get_serializer(games, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def ongoing_games(self, request):
        """Get ongoing games for the current user"""
        user = self.request.user
        
        # Update all game statuses before returning
        Game.update_all_game_statuses()
        
        if hasattr(user, 'organizer'):
            # For organizers, show their ongoing games
            games = Game.objects.filter(organizer=user.organizer, status='ONGOING')
        elif hasattr(user, 'player'):
            # For players, show ongoing games they're participating in
            games = Game.objects.filter(participants=user.player, status='ONGOING')
        else:
            games = Game.objects.none()
        
        serializer = self.get_serializer(games, many=True)
        return Response(serializer.data) 