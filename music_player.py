import random
import keyboard
import time
import threading

class MusicPlayer:
    def __init__(self, spotify_client, macro_manager):
        self.spotify_client = spotify_client
        self.macro_manager = macro_manager
        self.last_played = {}
        self.playback_thread = None
        self.stop_event = threading.Event()
        self.is_paused = False

    def play_macros(self):
        print("Press 'esc' to return to the main menu.")
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'esc':
                    self.stop_event.set()
                    if self.playback_thread and self.playback_thread.is_alive():
                        self.playback_thread.join()
                    break
                elif event.name == 'space':
                    self.toggle_playback()
                elif event.name in self.macro_manager.macros:
                    self.stop_event.set()
                    if self.playback_thread and self.playback_thread.is_alive():
                        self.playback_thread.join()
                    self.stop_event.clear()
                    self.playback_thread = threading.Thread(target=self.play_macro, args=(event.name,))
                    self.playback_thread.start()

    def play_macro(self, key):
        playlist_id = self.macro_manager.macros[key]
        tracks = self.spotify_client.get_playlist_tracks(playlist_id)
        track_uris = [track['track']['uri'] for track in tracks]
        track_names = {track['track']['uri']: track['track']['name'] for track in tracks}
        if key in self.last_played and len(track_uris) > 1:
            track_uris = [uri for uri in track_uris if uri != self.last_played[key]]
        if not track_uris:
            print("No other tracks available in the playlist.")
            return
        track_uri = random.choice(track_uris)
        self.spotify_client.play_track(track_uri)
        self.last_played[key] = track_uri
        print(f"Playing track: {track_names[track_uri]}")
        self.wait_for_track_to_finish()
        self.stop_playback()

    def wait_for_track_to_finish(self):
        while not self.stop_event.is_set():
            playback = self.spotify_client.sp.current_playback()
            if playback is None or not playback['is_playing']:
                break
            time.sleep(1)

    def stop_playback(self):
        playback = self.spotify_client.sp.current_playback()
        if playback and playback['is_playing']:
            try:
                self.spotify_client.stop_playback()
            except spotipy.exceptions.SpotifyException as e:
                if e.http_status == 403:
                    print("Unable to stop playback: Permission denied.")
                else:
                    raise e

    def toggle_playback(self):
        playback = self.spotify_client.sp.current_playback()
        if playback and playback['is_playing']:
            self.spotify_client.stop_playback()
            self.is_paused = True
        elif self.is_paused:
            self.spotify_client.sp.start_playback()
            self.is_paused = False