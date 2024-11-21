# views.py

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Stream, ChatMessage
from .serializers import StreamSerializer, ChatMessageSerializer
from django.utils import timezone
from rest_framework.exceptions import NotFound

class StreamViewSet(viewsets.ModelViewSet):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer

    def get_object(self):
        slug = self.kwargs.get("slug")
        try:
            return Stream.objects.get(slug=slug)
        except Stream.DoesNotExist:
            raise NotFound("Stream not found.")

    @action(detail=True, methods=['post'], url_path='start')
    def start(self, request, slug=None):
        stream = self.get_object()
        stream.start_time = timezone.now()
        stream.is_live = True
        stream.save()
        return Response({'status': 'stream started'})

    @action(detail=True, methods=['post'], url_path='stop')
    def stop(self, request, slug=None):
        stream = self.get_object()
        stream.end_time = timezone.now()
        stream.is_live = False
        stream.save()
        return Response({'status': 'stream stopped'})

class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)