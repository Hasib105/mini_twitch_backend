from mongoengine import Document, StringField, ReferenceField, BooleanField, DateTimeField, URLField
from django.utils.text import slugify
from uuid import uuid4
from datetime import datetime


# Assuming you have defined a custom User document in MongoEngine

class Stream(Document):
    title = StringField(required=True, max_length=255)
    description = StringField(blank=True)
    streamer_username = StringField(required=True)  # Store User's username (from SQLite User)
    slug = StringField(unique=True, required=True)
    start_time = DateTimeField(default=datetime.now)
    end_time = DateTimeField(null=True)
    is_live = BooleanField(default=True)  # Indicates if the stream is live
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{uuid4().hex[:8]}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.streamer_username}"

    meta = {
        'collection': 'streams',  # MongoDB collection name
        'ordering': ['-start_time'],  # Order by latest streams first
    }

class ChatMessage(Document):
    stream_slug = StringField(required=True)  # Reference Stream by slug
    user = StringField(required=True)  # Store user's username
    message = StringField(required=True)
    timestamp = DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Message by {self.user} in stream {self.stream_slug}"

    meta = {
        'collection': 'chat_messages',  
        'ordering': ['-timestamp'],    
    }