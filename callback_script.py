#!/usr/bin/env python3
import os
import sys
import django
from datetime import timedelta

#chmod +x /path/to/callback_script.py

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'streaming_platform.settings')
django.setup()

from core.models import Stream

def update_stream_recording(recording_path):
    # Extract stream key from the filename
    filename = os.path.basename(recording_path)
    stream_key = filename.split('-')[0]

    try:
        # Find the stream in the database
        stream = Stream.objects.get(stream_key=stream_key)

        # Calculate duration from start and end times
        if stream.start_time and stream.end_time:
            duration = stream.end_time - stream.start_time
        else:
            duration = None

        # Update the stream with recording details
        relative_path = os.path.relpath(recording_path, '/path/to/your/project/media')
        stream.recording_path = f"recordings/{relative_path}"
        stream.duration = duration
        stream.save()

        print(f"Updated stream {stream.title} with recording {relative_path}")
    except Stream.DoesNotExist:
        print(f"Stream with key {stream_key} not found.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: callback_script.py <recording_path>")
        sys.exit(1)

    recording_path = sys.argv[1]
    update_stream_recording(recording_path)