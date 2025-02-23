from rest_framework import serializers
from core.models import AiChatSession

class AiChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiChatSession
        fields = ['id', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
