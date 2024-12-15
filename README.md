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

1. Install Python dependencies:

   ```bash
   pip install vlc pillow schedule customtkinter
