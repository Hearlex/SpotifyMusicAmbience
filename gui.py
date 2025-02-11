from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button, Header, Footer, Static, Input, Select
from spotify_client import SpotifyClient
from macro_manager import MacroManager
from music_player import MusicPlayer
import threading
import os
from dotenv import load_dotenv

class SpotifyApp(App):
    CSS_PATH = "gui.css"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        load_dotenv()
        print("SPOTIFY_CLIENT_ID:", os.getenv("SPOTIFY_CLIENT_ID"))
        print("SPOTIFY_CLIENT_SECRET:", os.getenv("SPOTIFY_CLIENT_SECRET"))
        print("SPOTIFY_REDIRECT_URI:", os.getenv("SPOTIFY_REDIRECT_URI"))
        self.spotify_client = SpotifyClient()
        self.macro_manager = MacroManager(self.spotify_client)
        self.music_player = MusicPlayer(self.spotify_client, self.macro_manager)
        self.playback_thread = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("Spotify Music Ambience", id="title"),
            Button("Set up key macros", id="setup_macros"),
            Button("Play music macros", id="play_macros"),
            Button("Exit", id="exit"),
            id="main_menu"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "setup_macros":
            self.setup_macros()
        elif button_id == "play_macros":
            self.play_macros()
        elif button_id == "exit":
            self.exit()

    def setup_macros(self):
        self.clear()
        playlists = self.spotify_client.get_playlists()
        options = [(playlist['id'], playlist['name']) for playlist in playlists]
        self.mount(Select(options=options, id="playlist_select"))
        self.mount(Input(placeholder="Enter key for macro", id="macro_key"))
        self.mount(Button("Add Macro", id="add_macro"))
        self.mount(Button("Back to Main Menu", id="back_to_main"))

    def play_macros(self):
        self.clear()
        self.mount(Static("Press 'esc' to return to the main menu."))
        self.playback_thread = threading.Thread(target=self.music_player.play_macros)
        self.playback_thread.start()

    def exit(self):
        self.exit()

    def clear(self):
        for widget in self.query("*"):
            widget.remove()

if __name__ == "__main__":
    SpotifyApp().run()
