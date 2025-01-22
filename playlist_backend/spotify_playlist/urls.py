from django.urls import path
from . import apis

urlpatterns = [
    path('login/', apis.spotify_login, name='login'),
    path('call_back/', apis.spotify_callback, name='call_back'),
    path('refresh_token/', apis.refresh_token, name='refresh_token'),
    path('create_playlist/', apis.create_playlist, name='create_playlist'),
]