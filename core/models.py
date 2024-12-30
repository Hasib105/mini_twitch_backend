from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from uuid import uuid4
from datetime import datetime

class Stream(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    streamer = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    stream_key = models.CharField(max_length=255, unique=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_live = models.BooleanField(default=False)
    recording_path = models.FileField(upload_to='recordings/', blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.title)}-{uuid4().hex[:8]}"
        if not self.stream_key:
            self.stream_key = uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.streamer.username}"

    class Meta:
        ordering = ['-start_time']

class ChatMessage(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message} in {self.stream.title}"