# Music Player Application

A music player application built using Python and the `vlc` library for media playback. The app allows users to control playback (play, pause, rewind, fast forward), manage playlists, adjust volume, apply equalizer settings, and more.

## Features

- Play, pause, and skip songs.
- Shuffle and repeat songs in the playlist.
- Control volume and playback position using a slider.
- Visual equalizer with preamp and band frequency controls.
- Customizable UI with small and fullscreen modes.
- Support for video playback (if applicable).
- Playlist management.

## Requirements

- Python 3.x
- VLC media player (with Python bindings)
- `tkinter` for the GUI
- `schedule` for task scheduling
- `Pillow` for image handling
- `ctk` for custom widgets (or replace with `tkinter` components)

## Installation

Install Python dependencies:

  ```bash
pip install python-vlc pillow schedule customtkinter
 ```
## Usage

1. **Starting the Application**:
   - Call the `start()` function to initialize the main window and begin music playback.

2. **Media Control**:
   - **Play/Pause**: Click on the play/pause button to control playback.
   - **Fast Forward/Rewind**: Use the keyboard shortcuts or UI buttons to fast forward or rewind the song.
   - **Next/Previous**: Skip to the next or previous song using the buttons or keyboard shortcuts.

3. **Volume Control**:
   - Use the volume slider to adjust the audio volume.

4. **Equalizer**:
   - Open the equalizer window to adjust the preamp and frequency bands for audio output.

5. **Playlist Management**:
   - The application supports playlist control with shuffle, repeat, and queue management.

6. **Fullscreen and Small Window Modes**:
   - Switch between fullscreen and small window modes for a better viewing experience.

7. **Close the Application**:
   - Use the `ee()` function to stop the application and close all open windows.

## Key Bindings

- **Space/Return**: Play/Pause the current song.
- **Left/Alt+Left/b**: Rewind the current song by 10 seconds.
- **Right/Alt+Right**: Fast forward the current song by 10 seconds.
- **n**: Skip to the next song.
- **p**: Open the playlist window.
- **e**: Open the equalizer window.
- **r**: Toggle repeat mode.
- **s**: Shuffle the playlist.

## Screenshots

![Screenshot 2024-12-11 151648](https://github.com/user-attachments/assets/bdcd1bf5-7611-4cea-9f15-9ceb0a6455ad)

