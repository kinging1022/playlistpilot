from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse , JsonResponse # For error handling
from django.views.decorators.csrf import ensure_csrf_cookie

from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import secrets
import urllib.parse
import base64
import logging

logger = logging.getLogger(__name__)


auth_dict = {}


SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"
uris = []


@api_view(['GET'])
def spotify_login(request):
    scope = "playlist-modify-public playlist-modify-private"

    params = {
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
    }

    auth_url = f"{SPOTIFY_AUTH_URL}?{urllib.parse.urlencode(params)}"

    return Response({'auth_url':auth_url})

@api_view(['GET'])
def spotify_callback(request):
    code = request.GET.get('code')
    print(f"code{code}")

    
    if not code: 
        return JsonResponse({'error': 'Invalid callback parameters or CSRF protection failure'}, status=400)
    
    auth_header = base64.b64encode(
        f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}".encode()
    ).decode()

    try:
        response = requests.post(
            SPOTIFY_TOKEN_URL,
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
            },
            headers={'Authorization': f'Basic {auth_header}'}
        )
        
        response.raise_for_status()
        
        tokens = response.json()

        auth_dict['access_token'] = tokens['access_token']
        auth_dict['refresh_token'] = tokens['refresh_token']
        auth_dict['expires_at'] = datetime.now().timestamp() + tokens['expires_in']

        
        # Redirect to frontend with success status
        frontend_url = settings.SUCCESS_URL
        return redirect(frontend_url)

    except requests.exceptions.RequestException as e:
        logger.error(f"Error exchanging code for tokens: {e}")
        return JsonResponse({'error': f'Failed to get token: {str(e)}'}, status=400)



@api_view(['POST'])
def create_playlist(request): 
    
    token = auth_dict['access_token']
    
    playlist_name = request.data.get('name', 'New Playlist')
    description = request.data.get('description', 'Created via PlaylistPilot')
    is_public = request.data.get('public', True)
    song_list = request.data.get('song_list', [])

    try:
        # Create playlist
        response = requests.post(
            f"{SPOTIFY_API_URL}/me/playlists",
            headers={'Authorization': f'Bearer {token}'},
            json={
                'name': playlist_name,
                'description': description,
                'public': is_public
            }
        )
        response.raise_for_status()
        playlist = response.json()
        
        # Add tracks if provided
        if song_list and playlist['id']:
            track_uris = []
            for song in song_list:
                search_response = requests.get(
                    f"{SPOTIFY_API_URL}/search",
                    headers={'Authorization': f'Bearer {token}'},
                    params={
                        'q': f"track:{song['title']} artist:{song['artist']}",
                        'type': 'track',
                        'limit': 1
                    }
                )
                if search_response.status_code == 200:
                    tracks = search_response.json().get('tracks', {}).get('items', [])
                    if tracks:
                        track_uris.append(tracks[0]['uri'])
            
            if track_uris:
                requests.post(
                    f"{SPOTIFY_API_URL}/playlists/{playlist['id']}/tracks",
                    headers={'Authorization': f'Bearer {token}'},
                    json={'uris': track_uris}
                )
        
        return Response({
            'success': True,
            'playlist_url': playlist['external_urls']['spotify']
        })
        
    except requests.exceptions.RequestException as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








def refresh_token(request):
    refresh_token = auth_dict.get('refresh_token')
    if not refresh_token:
        return redirect('login')
    
    auth_header = base64.b64encode(
        f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}".encode()
    ).decode()
    
    response = requests.post(
        SPOTIFY_TOKEN_URL,
        data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        },
        headers={'Authorization': f'Basic {auth_header}'}
    )
    
    if response.status_code == 200:
        tokens = response.json()
        request.session['access_token'] = tokens['access_token']
        request.session['expires_at'] = datetime.now().timestamp() + tokens['expires_in']
        return Response({'message': 'Token refreshed'})
    return redirect('login')

