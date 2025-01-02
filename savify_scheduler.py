import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import schedule
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Use .env to set these variables
def get_client(client_id, client_secret, redirect_uri, scope, user=None, refresh_token=None):
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        username=user
    )
    
    if refresh_token:
        auth_manager.refresh_access_token(refresh_token)

    client = spotipy.Spotify(auth_manager=auth_manager)
    return client

# Scrape the playlist tracks (not through Spotify API, as Discover Weekly's are not accessible)
def scrape_playlist_tracks(public_url):
    response = requests.get(public_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        track_elements = soup.find_all('div', class_='Box__BoxComponent-sc-y4nds-0')
        
        tracks = []
        for track in track_elements:
            # The specific classes that are used by Spotify, but chances are they change over time
            track_name_element = track.find('span', class_='ListRowTitle__LineClamp-sc-1xe2if1-0')
            artist_name_element = track.find('p', class_='ListRowDetails__ListRowDetailText-sc-sozu4l-0')

            if track_name_element and artist_name_element:
                track_name = track_name_element.get_text(strip=True)
                artist_name = artist_name_element.get_text(strip=True)
                tracks.append({'track': track_name, 'artist': artist_name})
        
        return tracks
    else:
        print(f"Failed to retrieve playlist. Status code: {response.status_code}")
        return []
    
# Use the track name and artist combination to get the URI for a track from the Spotify API
def get_track_uri(client, track_name, artist_name):
    search_results = client.search(q=f"track:{track_name} artist:{artist_name}", type="track")
    if search_results["tracks"]["items"]:
        return search_results["tracks"]["items"][0]["uri"]
    else:
        print(f"Track not found: {track_name} by {artist_name}")
        return None

# Get the discover weekly tracks and return the track URIs
def get_discover_weekly_tracks(client, public_playlist_url):
    discover_weekly_tracks = []
    for track in scrape_playlist_tracks(public_playlist_url):
        track_uri = get_track_uri(client=client, track_name=track['track'], artist_name=track['artist'])
        if track_uri:
            discover_weekly_tracks.append(track_uri)

    return discover_weekly_tracks

# Determine the date of the archived Discover Weekly playlist
def get_discover_weekly_date():
    created_date = datetime.now()
    return created_date.strftime("%d-%m-%y")

# Centralized function for playlist naming
def get_playlist_name():
    date = get_discover_weekly_date()
    return f"[ARCH] DW {date}"

# Check if a playlist for the current week already exists
def playlist_exists(client, user):
    playlist_name = get_playlist_name()
    playlists = client.user_playlists(user)
    for playlist in playlists["items"]:
        if playlist["name"] == playlist_name:
            return True
    return False

# Create a new playlist for the archived Discover Weekly playlist
def create_new_playlist(client, user):
    playlist_name = get_playlist_name()
    new_playlist = client.user_playlist_create(
        user=user,
        name=playlist_name,
        public=False,
        description=f"Archived Discover Weekly playlist for week of {get_discover_weekly_date()}",
    )
    return new_playlist

# Put the current Discover Weekly tracks into the new playlist
def archive_discover_weekly(client, user, new_playlist, public_playlist_url):
    client.user_playlist_add_tracks(
        user=user,
        playlist_id=new_playlist["id"],
        tracks=get_discover_weekly_tracks(client=client, public_playlist_url=public_playlist_url),
    )

# Main task for weekly scheduling
def archive_discover_weekly_task():
    load_dotenv()

    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
    SOURCE_PLAYLIST_PUBLIC_URL = os.getenv('SOURCE_PLAYLIST_PUBLIC_URL') # Mostly intended for a Spotify Created Discover Weekly playlist, but can be used for any public playlist

    client = get_client(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=["playlist-read-private", "playlist-modify-private"]
    )

    user_id = client.current_user()["id"]

    # Check for duplicates
    if playlist_exists(client, user_id):
        print(f"Playlist for the week of {get_discover_weekly_date()} already exists. Skipping...")
        return

    # Create and archive
    new_playlist = create_new_playlist(client, user_id)
    archive_discover_weekly(client, user_id, new_playlist, SOURCE_PLAYLIST_PUBLIC_URL)
    print(f"Archived Discover Weekly for the week of {get_discover_weekly_date()}")


# Use of schedule library to determine when to run the task
schedule.every().monday.at("04:00").do(archive_discover_weekly_task)

if __name__ == "__main__":
    print("Discover Weekly archiver is running...")
    while True:
        schedule.run_pending()
        time.sleep(1)
