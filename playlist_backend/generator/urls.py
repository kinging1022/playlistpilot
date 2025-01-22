from django.urls import path
from . import apis

urlpatterns = [
    path('time-machine/', apis.get_billboard_hot_100, name='generate_billboard_hot_100'),
    path('ai-generator/', apis.get_ai_playlist, name='ai_generator'),
]