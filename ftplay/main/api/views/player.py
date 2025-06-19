from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.player import (
    PlayerProfileSerializer, 
    PlayerProfileUpdateSerializer,
    PlayerRankScoreUpdateSerializer,
    PlayerDeleteSerializer
)

class PlayerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'player'):
            return Response(
                {'error': 'User is not a player'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PlayerProfileSerializer(request.user.player)
        return Response(serializer.data)

    def put(self, request):
        if not hasattr(request.user, 'player'):
            return Response(
                {'error': 'User is not a player'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PlayerProfileUpdateSerializer(
            request.user.player,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(PlayerProfileSerializer(request.user.player).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if not hasattr(request.user, 'player'):
            return Response(
                {'error': 'User is not a player'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Validate password confirmation
        serializer = PlayerDeleteSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            # Delete the player and associated user
            user = request.user
            user.delete()  # This will also delete the player due to CASCADE
            
            return Response({
                'message': 'Player account deleted successfully'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlayerRankScoreView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        if not hasattr(request.user, 'player'):
            return Response(
                {'error': 'User is not a player'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PlayerRankScoreUpdateSerializer(
            request.user.player,
            data=request.data
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Rank scores updated successfully',
                'scores': serializer.validated_data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 