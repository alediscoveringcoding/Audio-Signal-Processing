import numpy as np
import wave
import winsound
import struct

SAMPLE_RATE = 44100

def midi_to_frequency(midi_note):
    return 440.0 * (2 ** ((midi_note - 69) / 12))

def save_and_play_note(midi_note, duration=0.4):
    freq = midi_to_frequency(midi_note)
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    wave_data = 0.2 * np.sin(2 * np.pi * freq * t)
    
    filename = "temp_note.wav"
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        for sample in wave_data:
            wf.writeframesraw(struct.pack('<h', int(sample * 32767)))
    
    winsound.PlaySound(filename, winsound.SND_FILENAME)

# Notele pentru Happy Birthday conform documentului [cite: 217-228]
# Mapare note nume -> MIDI: G3=55, A4=69, B4=71, C4=60, D4=62
melody_midi = [55, 55, 69, 55, 60, 71, 55, 55, 69, 55, 62, 60]

print("Redăm: Happy Birthday...")
for note in melody_midi:
    save_and_play_note(note)