import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json

class SpotifyClient:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
            scope="user-library-read playlist-read-private user-modify-playback-state user-read-playback-state"
        ))
        self.device_file = 'default_device.json'
        self.default_device = self.load_default_device()

    def get_playlists(self):
        playlists = self.sp.current_user_playlists()
        return playlists['items']

    def get_playlist_tracks(self, playlist_id):
        tracks = self.sp.playlist_tracks(playlist_id)
        return tracks['items']

    def get_devices(self):
        devices = self.sp.devices()
        return devices['devices']

    def set_default_device(self, device_id):
        self.default_device = device_id
        with open(self.device_file, 'w') as f:
            json.dump({'device_id': device_id}, f)

    def load_default_device(self):
        try:
            with open(self.device_file, 'r') as f:
                data = json.load(f)
                return data.get('device_id')
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def play_track(self, track_uri):
        devices = self.sp.devices()
        if not devices['devices']:
            print("No active device found. Please start Spotify on one of your devices.")
            return

        # Try to use default device if available
        if self.default_device:
            device_ids = [d['id'] for d in devices['devices']]
            if self.default_device in device_ids:
                self.sp.transfer_playback(device_id=self.default_device, force_play=True)
                self.sp.start_playback(device_id=self.default_device, uris=[track_uri])
                return

        # Fall back to previous behavior if default device is not available
        active_device = None
        for device in devices['devices']:
            if device['is_active']:
                active_device = device['id']
                break
        if not active_device:
            active_device = devices['devices'][0]['id']
            self.sp.transfer_playback(device_id=active_device, force_play=True)
        self.sp.start_playback(device_id=active_device, uris=[track_uri])

    def stop_playback(self):
        try:
            self.sp.pause_playback()
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 403:
                print("Unable to stop playback: Permission denied.")
            else:
                raise e
