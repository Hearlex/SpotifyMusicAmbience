import os
from dotenv import load_dotenv
from spotify_client import SpotifyClient
from macro_manager import MacroManager
from music_player import MusicPlayer


def select_default_device(spotify_client):
    devices = spotify_client.get_devices()
    if not devices:
        print("No devices found. Please start Spotify on one of your devices.")
        return
    
    print("\nAvailable devices:")
    for idx, device in enumerate(devices):
        print(f"{idx + 1}. {device['name']} ({device['type']})")
    
    try:
        choice = int(input("\nChoose a device number (or 0 to cancel): ")) - 1
        if choice == -1:
            return
        if 0 <= choice < len(devices):
            spotify_client.set_default_device(devices[choice]['id'])
            print(f"Default device set to: {devices[choice]['name']}")
        else:
            print("Invalid device number.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def main():
    load_dotenv()
    spotify_client = SpotifyClient()
    macro_manager = MacroManager(spotify_client)
    music_player = MusicPlayer(spotify_client, macro_manager)

    while True:
        print("\nMain Menu:")
        print("1. Set up key macros")
        print("2. Play music macros")
        print("3. Select default device")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            macro_manager.setup_macros()
        elif choice == '2':
            music_player.play_macros()
        elif choice == '3':
            select_default_device(spotify_client)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
