# AudioBox

AudioBox allows the user to play music and sound effects on any platform as long as you have the files.

## Latest Updates: 
* Made `sfx()` play in a separate thread like `play_music()`.
* Added functions to manage playlists: `remove_from_playlist()` and `clear_playlist()`.

## Installation

Install via pip:

```bash
pip install audiobox
```

## Example Code: 

```python
from time import sleep as wait
from audiobox import generate_example_files, sfx, play_music, get_audio_length, add_to_playlist, remove_from_playlist, clear_playlist, play_playlist

# Generate example files
generate_example_files()

# Play sound effect in a separate thread
sfx("example_sfx", times=1, volume=0.5)
wait(get_audio_length("example_sfx"))

# Play music with looping enabled
play_music("example_music", stop_other=True, loop=True)

# Wait for the duration of the music
wait(get_audio_length("example_music"))

# Manage playlist: Add, Remove, Clear
add_to_playlist("example_music")
play_playlist()
remove_from_playlist("example_music")
clear_playlist()
```

## Links: 
### Website: https://tairerullc.vercel.app/

#### Contact 'tairerullc@gmail.com' for any inquiries, and we will get back to you at our earliest convenience. Thank you for using our product, and happy coding!