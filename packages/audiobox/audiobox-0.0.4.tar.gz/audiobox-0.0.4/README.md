# AudioBox

AudioBox allows the user to play music and sound effects on any platform as long as you have the files.

## Latest Updates: 
* Made sfx play in a seperate thread like music

## Installation

Install via pip:

```bash
pip install audiobox
```

Example code: 

```py
from time import sleep as wait
from threading import Thread
from audiobox import generate_example_files, sfx, play_music, get_audio_length

# Generate example files
generate_example_files()

# Play sound effect
sfx("example_sfx", times=1, volume=0.5)
wait(get_audio_length("example_sfx"))

# Play music with looping enabled
play_music("example_music", stop_other=True, loop=True)

# Wait for the duration of the music
wait(get_audio_length("example_music"))
```

## Links: 
### Website: https://tairerullc.vercel.app/


#### Contact 'tairerullc@gmail.com' for any inquires and we will get back at our latest expense. Thank you for using our product and happy coding!