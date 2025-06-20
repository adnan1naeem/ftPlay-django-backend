from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.organizer import (
    OrganizerProfileSerializer, 
    OrganizerProfileUpdateSerializer,
    OrganizerDeleteSerializer
)

class OrganizerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'organizer'):
            return Response(
                {'error': 'User is not an organizer'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = OrganizerProfileSerializer(request.user.organizer)
        return Response(serializer.data)

    def put(self, request):
        if not hasattr(request.user, 'organizer'):
            return Response(
                {'error': 'User is not an organizer'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = OrganizerProfileUpdateSerializer(
            request.user.organizer, 
            data=request.data, 
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Organizer profile updated successfully',
                'data': OrganizerProfileSerializer(request.user.organizer).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if not hasattr(request.user, 'organizer'):
            return Response(
                {'error': 'User is not an organizer'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = OrganizerDeleteSerializer(
            data=request.data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            # Delete the organizer and user
            user = request.user
            user.delete()  # This will cascade delete the organizer
            
            return Response({
                'message': 'Organizer account deleted successfully'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 