import json
import os

class MacroManager:
    def __init__(self, spotify_client):
        self.spotify_client = spotify_client
        self.macro_file = 'macros.json'
        self.macros = self.load_macros()

    def load_macros(self):
        if os.path.exists(self.macro_file):
            with open(self.macro_file, 'r') as file:
                return json.load(file)
        return {}

    def save_macros(self):
        with open(self.macro_file, 'w') as file:
            json.dump(self.macros, file, indent=4)

    def setup_macros(self):
        while True:
            print("Macro Setup Menu:")
            print("1. Add new macro")
            print("2. Change existing macro")
            print("3. Remove macro")
            print("4. Return to main menu")
            choice = input("Choose an option: ")

            if choice == '1':
                self.add_macro()
            elif choice == '2':
                self.change_macro()
            elif choice == '3':
                self.remove_macro()
            elif choice == '4':
                self.save_macros()
                break
            else:
                print("Invalid choice. Please try again.")

    def add_macro(self):
        playlists = self.spotify_client.get_playlists()
        for idx, playlist in enumerate(playlists):
            print(f"{idx + 1}. {playlist['name']}")
        playlist_choice = int(input("Choose a playlist: ")) - 1
        playlist_id = playlists[playlist_choice]['id']
        key = input("Enter the key for the macro: ")
        self.macros[key] = playlist_id

    def change_macro(self):
        key = input("Enter the key of the macro to change: ")
        if key in self.macros:
            playlists = self.spotify_client.get_playlists()
            for idx, playlist in enumerate(playlists):
                print(f"{idx + 1}. {playlist['name']}")
            playlist_choice = int(input("Choose a new playlist: ")) - 1
            playlist_id = playlists[playlist_choice]['id']
            self.macros[key] = playlist_id
        else:
            print("Macro not found.")

    def remove_macro(self):
        key = input("Enter the key of the macro to remove: ")
        if key in self.macros:
            del self.macros[key]
        else:
            print("Macro not found.")
