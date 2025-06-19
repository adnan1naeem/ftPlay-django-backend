from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from ..serializers.game import GameSerializer, GameRatingSerializer, GameCommentSerializer
from main.models import Game, GameRating, GameComment

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        game = self.get_object()
        # Add join game logic here
        return Response({'message': 'Successfully joined the game'})

    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        game = self.get_object()
        serializer = GameRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(game=game)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        game = self.get_object()
        serializer = GameCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(game=game)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 