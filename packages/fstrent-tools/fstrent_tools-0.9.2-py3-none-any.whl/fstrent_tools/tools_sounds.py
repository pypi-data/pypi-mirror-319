import time
from fstrent_colors import cp
import os
import pkg_resources
import numpy as np

__all__ = [
    'beep',
    'play_beep',
    'play_file',
    'play_cash',
    'play_doh',
    'play_sw_theme',
    'play_sw_imperial_march',
    'play_thunder'
]

# Alternative sound libraries for cross-platform support
try:
    import simpleaudio as sa  # for playing wav files
except ImportError:
    sa = None

def beep(reps=1):
    for _ in range(0, reps, 1):
        cp('beep()!!!', font='white', bg_color='red')
    play_beep(frequency=2500,duration=1000, reps=reps)

def play_beep(frequency=1000, duration=1000, reps=1):
    """
    Used to play a beep sound
    :param frequency: The frequency of the beep in Hz
    :type frequency: int
    :param duration: The duration of the beep in milliseconds
    :type duration: int
    :param reps: Number of times to repeat the beep
    :type reps: int
    """
    if sa:
        # Convert duration to seconds for numpy
        duration_s = duration / 1000.0
        
        # Generate time array for one beep
        sample_rate = 44100
        t = np.linspace(0, duration_s, int(sample_rate * duration_s))
        
        # Generate sine wave
        samples = (np.sin(2 * np.pi * frequency * t) * 32767).astype(np.int16)
        
        # Play the beep the specified number of times
        for _ in range(reps):
            wave_obj = sa.WaveObject(samples, 1, 2, sample_rate)
            play_obj = wave_obj.play()
            play_obj.wait_done()
    else:
        print(f'Warning: Beep sound not supported - simpleaudio not available (frequency={frequency}, duration={duration}, reps={reps})')

def play_file(f):
    """
    Play a WAV file using available sound library
    """
    if sa:
        wave_obj = sa.WaveObject.from_wave_file(f)
        play_obj = wave_obj.play()
        play_obj.wait_done()

def play_cash():
    print('play_cash()')
    play_file(get_sound_path('cashreg.wav'))

def play_doh():
    print('play_doh()')
    play_file(get_sound_path('DOH!.WAV'))

def play_sw_theme():
    """
    Used to play the Star Wars theme song
    """
    play_beep(1046, 880)
    play_beep(1567, 880)
    play_beep(1396, 55)
    play_beep(1318, 55)
    play_beep(1174, 55)
    play_beep(2093, 880)
    time.sleep(0.3)
    play_beep(1567, 600)
    play_beep(1396, 55)
    play_beep(1318, 55)
    play_beep(1174, 55)
    play_beep(2093, 880)
    time.sleep(0.3)
    play_beep(1567, 600)
    play_beep(1396, 55)
    play_beep(1318, 55)
    play_beep(1396, 55)
    play_beep(1174, 880)

def play_sw_imperial_march():
    """
    Used to play the Star Wars Imperial March song
    """
    play_beep(440, 500)
    play_beep(440, 500)
    play_beep(440, 500)
    play_beep(349, 375)
    play_beep(523, 150)
    play_beep(440, 600)
    play_beep(349, 375)
    play_beep(523, 150)
    play_beep(440, 1000)
    time.sleep(0.2)
    play_beep(659, 500)
    play_beep(659, 500)
    play_beep(659, 500)
    play_beep(698, 375)
    play_beep(523, 150)
    play_beep(415, 600)
    play_beep(349, 375)
    play_beep(523, 150)
    play_beep(440, 1000)

def play_thunder():
    print('play_thunder()')
    play_file(get_sound_path('thunder.wav'))

def get_sound_path(filename):
    return pkg_resources.resource_filename('fstrent_tools', os.path.join('..', 'sounds', filename))

