from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StreamViewSet, ChatMessageViewSet

# Register ViewSets with the router
router = DefaultRouter()
router.register(r'streams', StreamViewSet, basename='stream')
router.register(r'chat', ChatMessageViewSet, basename='chat')

# URL patterns
urlpatterns = [
    # Authentication endpoints using Djoser
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # Include all endpoints registered with the router
    path('', include(router.urls)),
]
