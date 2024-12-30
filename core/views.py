# views.py

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Stream, ChatMessage
from .serializers import StreamSerializer, ChatMessageSerializer
from django.utils import timezone
from rest_framework.exceptions import NotFound

class StreamViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing Stream objects.
    """
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    lookup_field = 'slug'  # Enables lookup by slug instead of id

    def create(self, request, *args, **kwargs):
        """
        Override create to handle stream creation explicitly.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.validated_data['streamer'] = request.user
        stream = serializer.save()  # Save the stream and auto-generate slug/stream_key
        return Response(
            {
                "message": "Stream created successfully.",
                "stream": StreamSerializer(stream).data
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'], url_path='start')
    def start(self, request, slug=None):
        """
        Start the stream by setting it to live and recording the start time.
        """
        stream = self.get_object()
        if stream.is_live:
            raise ValidationError({"error": "Stream is already live."})
        stream.start_time = timezone.now()
        stream.is_live = True
        stream.save()
        return Response({"message": "Stream started successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='stop')
    def stop(self, request, slug=None):
        """
        Stop the stream by setting it offline and recording the end time.
        """
        stream = self.get_object()
        if not stream.is_live:
            raise ValidationError({"error": "Stream is not live."})
        stream.end_time = timezone.now()
        stream.is_live = False
        # Calculate duration
        if stream.start_time:
            stream.duration = stream.end_time - stream.start_time
        stream.save()
        return Response({"message": "Stream stopped successfully."}, status=status.HTTP_200_OK)

class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)