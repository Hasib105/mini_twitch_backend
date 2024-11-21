from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import StreamViewSet, ChatMessageViewSet

router = DefaultRouter()
router.register(r'streams', StreamViewSet, basename='stream')
router.register(r'chat', ChatMessageViewSet, basename='chat')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
    path('streams/<slug:slug>/', StreamViewSet.as_view({'post': 'start'}), name='start_stream'),
    path('streams/<slug:slug>/stop/', StreamViewSet.as_view({'post': 'stop'}), name='stop_stream'),
]


