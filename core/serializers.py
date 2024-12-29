# serializers.py

from rest_framework import serializers
from .models import Stream, ChatMessage

class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = [
            'title',
            'description',
            'streamer',
            'slug',
            'stream_key',
            'start_time',
            'end_time',
            'is_live',
            'recording_path',
            'duration',
        ]
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'