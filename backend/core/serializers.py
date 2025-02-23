from rest_framework import serializers
from core.models import AiChatSession


class AiChatSessionMessageSerializer(serializers.Serializer):
    role = serializers.CharField()
    content = serializers.CharField()


class AiChatSessionSerializer(serializers.ModelSerializer):
    messages = AiChatSessionMessageSerializer(many=True)

    class Meta:
        model = AiChatSession
        fields = ['id', 'messages']
        read_only_fields = ['messages']
