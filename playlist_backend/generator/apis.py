import google.generativeai as genai
import time
import random
from django.conf import settings
from django.shortcuts import redirect

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
import requests







@api_view(['GET'])
def get_billboard_hot_100(request):
    date = request.query_params.get('date')
    if date is None:
        return Response({"error": "date query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
    url = "https://www.billboard.com/charts/hot-100/" + date
    response = requests.get(url=url, headers=header)

    time.sleep(random.uniform(1,3))

    songs = []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    song_list = soup.select("li ul li")
    for item in song_list:
        
        h3_tag = item.find('h3')
        if h3_tag:
            
            
            song_title = h3_tag.getText(strip=True)

            span_tag = h3_tag.find_next("span")

            artist_name = span_tag.getText(strip=True) if span_tag else "unknown"

            songs.append({
                'title': song_title,
                'artist' : artist_name
            })

    return Response({"songs":songs})




@api_view(['GET'])
def get_ai_playlist(request):
    prompt = request.query_params.get('prompt')
    song_count = request.query_params.get('song_count')
    if prompt is None:
        return Response({'error': 'prompt query is required'}, 
                      status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Configure Gemini API
        genai.configure(api_key=settings.GEMINI_SECRET_KEY)
        model = genai.GenerativeModel('gemini-pro')

        # Generate response
        response = model.generate_content(
            f"""Generate a playlist of {song_count} songs based on this theme: {prompt}
            Format each line exactly like this: Song Title - Artist Name
            Only provide the song list, no other text."""
        )
        playlist = []
        if response.text:
            lines = response.text.strip().split('\n')
            for line in lines:
                if '-' in line:
                    song, artist = line.split('-', 1)
                    if song and artist:
                        playlist.append({
                            'title': song.strip(),
                            'artist': artist.strip()
                        })

        if not playlist:
            return Response(
                {"error": "Could not generate playlist"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({"playlist": playlist})

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    



