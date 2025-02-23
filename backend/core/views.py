from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import AiChatSession
from core.serializers import AiChatSessionSerializer


@api_view(['POST'])
def create_chat_session(request):
    """Create a new chat session."""
    session = AiChatSession.objects.create()
    serializer = AiChatSessionSerializer(session)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
