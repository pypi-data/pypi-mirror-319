import os
import sys
import shutil
from threading import Thread
from time import sleep as wait
from typing import Optional, Callable, List, Dict
import pygame
from mutagen.mp3 import MP3

# Redirect stdout to suppress pygame and AltColor messages
old_stdout: Optional[object] = sys.stdout
sys.stdout = open(os.devnull, 'w')

# Initialize the pygame mixer
pygame.mixer.init()

# Retrieve colored print
from altcolor import cPrint  # Custom color print module

# Restore stdout
sys.stdout.close()
sys.stdout = old_stdout

# Global variables
music_on: bool = True  # Flag indicating if music playback is enabled
music_file: Optional[str] = None  # Currently playing music file
current_dir: str = os.path.dirname(__file__)  # Directory of the current script
playlist: List[str] = []  # List of music files for the playlist
sound_registry: Dict[str, pygame.mixer.Sound] = {}  # Cached sound effects

def show_credits() -> None:
    """
    Display credits and license information for the program.
    """
    cPrint("BLUE", "\n\nThanks for using AudioBox! Check out our other products at 'https://tairerullc.vercel.app'")
    cPrint(
        "MAGENTA",
        "\n\nNote:\nThe music, not the sfx, is by Sadie Jean. The song is called 'Locksmith' and is available via Spotify."
        "\nPlease note this song is copyrighted material, and we use it only as an example. "
        "We are not endorsed by them, nor are they endorsed by us.\n\n"
    )
show_credits()

def generate_example_files() -> None:
    """
    Generate two example audio files for use by the program.
    """
    example_sfx: str = os.path.join(current_dir, "example_sfx.wav")
    example_music: str = os.path.join(current_dir, "example_music.mp3")

    cloned_sfx: str = "example_sfx.wav"
    cloned_music: str = "example_music.mp3"

    try:
        shutil.copyfile(example_sfx, cloned_sfx)
        shutil.copyfile(example_music, cloned_music)
    except FileNotFoundError as e:
        print(f"Error: {e}. Example files not found.")

def sfx(filename: str, times: int = 1, volume: float = 0.5) -> None:
    """
    Play a sound effect a specified number of times with adjustable volume.

    Args:
        filename (str): The base name of the sound effect file (without extension).
        times (int): Number of times to play the sound effect (default is 1).
        volume (float): Volume level for the sound effect (0.0 to 1.0).
    """
    def play_sound_effect() -> None:
        filepath: str = find_audio_file(filename)
        try:
            if filename not in sound_registry:
                sound_registry[filename] = pygame.mixer.Sound(filepath)
            sound_effect = sound_registry[filename]
            sound_effect.set_volume(volume)
            sound_effect.play(loops=times - 1)
        except pygame.error as e:
            print(f"Error playing sound effect: {e}")

    sound_thread: Thread = Thread(target=play_sound_effect)
    sound_thread.start()

def play_music(filename: str, stop_other: bool = False, loop: bool = True) -> None:
    """
    Play background music, optionally stopping any currently playing music.

    Args:
        filename (str): The base name of the music file (without extension).
        stop_other (bool): Whether to stop other currently playing music (default is False).
        loop (bool): Whether to loop the music (default is True).
    """
    global music_file

    if not music_on:
        return

    filepath: str = find_audio_file(filename)

    if pygame.mixer.music.get_busy() and music_file == filepath:
        return  # Music already playing, no need to restart

    def play_and_wait() -> None:
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play(-1 if loop else 0)
            pygame.mixer.music.set_volume(1)
            music_file = filepath

            while pygame.mixer.music.get_busy():
                wait(1)
        except pygame.error as e:
            print(f"Error loading or playing music file: {e}")

    if stop_other:
        pygame.mixer.music.stop()

    music_thread: Thread = Thread(target=play_and_wait)
    music_thread.start()

def stop_music() -> None:
    """
    Stop the currently playing background music.
    """
    global music_file
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        music_file = None

def add_to_playlist(filename: str) -> None:
    """
    Add a music file to the playlist.

    Args:
        filename (str): The base name of the music file (without extension).
    """
    filepath: str = find_audio_file(filename)
    playlist.append(filepath)

def play_playlist() -> None:
    """
    Play all music files in the playlist sequentially.
    """
    def play_songs() -> None:
        for song in playlist:
            if music_on:
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    wait(1)

    playlist_thread: Thread = Thread(target=play_songs)
    playlist_thread.start()

def find_audio_file(filename: str) -> str:
    """
    Locate an audio file with .wav or .mp3 extension.

    Args:
        filename (str): The base name of the file to locate.

    Returns:
        str: The full path to the located audio file.

    Raises:
        FileNotFoundError: If neither a .wav nor .mp3 file with the given base name is found.
    """
    wav_file: str = f"{filename}.wav"
    mp3_file: str = f"{filename}.mp3"

    if os.path.isfile(wav_file):
        return wav_file
    elif os.path.isfile(mp3_file):
        return mp3_file
    else:
        raise FileNotFoundError(f"File {filename}.wav or {filename}.mp3 not found.")

def get_audio_length(filename: str) -> float:
    """
    Retrieve the length of an audio file in seconds.

    Args:
        filename (str): The base name of the audio file (without extension).

    Returns:
        float: The length of the audio file in seconds.

    Raises:
        FileNotFoundError: If the audio file is not found.
        ValueError: If the audio file format is unsupported.
    """
    filepath: str = find_audio_file(filename)
    if filepath.endswith(".wav"):
        try:
            sound = pygame.mixer.Sound(filepath)
            return sound.get_length()
        except pygame.error as e:
            raise ValueError(f"Error retrieving length for WAV file: {e}")
    elif filepath.endswith(".mp3"):
        try:
            audio = MP3(filepath)
            return audio.info.length
        except Exception as e:
            raise ValueError(f"Error retrieving length for MP3 file: {e}")
    else:
        raise ValueError("Unsupported file format. Only .wav and .mp3 are supported.")