# SpotifyMusicAmbience

A command-line tool that plays a random track from a specified Spotify playlist based on key macros.

## Features
- Play a random track from your favorite Spotify playlists.
- Set up custom keyboard macros to easily trigger playback.
- Manage default playback devices automatically.
- Convenient device selection and playback control.

## Prerequisites
- Python 3.6+
- A Spotify Developer account with a registered app.
- Installed Python packages: `spotipy`, `python-dotenv`, `keyboard`

## Installation
1. Clone the repository to your local machine.
2. Install the required dependencies via pip:
    ```
    pip install -r requirements.txt
    ```
3. Create a `.env` file in the project root with your Spotify credentials:
    ```
    SPOTIFY_CLIENT_ID=your_client_id
    SPOTIFY_CLIENT_SECRET=your_client_secret
    SPOTIFY_REDIRECT_URI=your_redirect_uri
    ```

## Setup
- **Configure Macros:** Run the application and use the menu to set up or modify key macros linked to your Spotify playlists.
- **Select Default Device:** Ensure your Spotify app is running on at least one device and select a default device from the provided menu.

## Usage
Run the main script:
```
python main.py
```
Follow the on-screen menu: 
- Set up key macros.
- Play music macros.
- Select default device.
- Exit the application.

## Notes
- Use the `esc` key to exit macro playback mode.
- Press `space` to toggle playback during macro mode.
- The app automatically remembers your last played track per macro to avoid repeats.

## License
Distributed under the MIT License.

## Contributing
Contributions and suggestions are welcome. Feel free to open issues or pull requests.
