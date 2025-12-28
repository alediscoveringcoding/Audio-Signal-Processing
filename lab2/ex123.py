import numpy as np
import wave
import winsound
import struct

# --- Configurare ---
A4_FREQ = 440.0
SAMPLE_RATE = 44100

# Conversie MIDI la Frecvență
def midi_to_frequency(midi_note):
    return A4_FREQ * (2 ** ((midi_note - 69) / 12))

# Generare Undă Sinusoidală
def generate_sine_wave(frequency, duration, amplitude=0.2):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    wave_data = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave_data

# Salvare WAV folosind doar modulul 'wave' (FĂRĂ SCIPY)
def save_wave_nativ(filename, wave_data):
    # Convertim datele în format binar (16-bit PCM)
    n_frames = len(wave_data)
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # Mono [cite: 85]
        wf.setsampwidth(2)  # 2 bytes per sample (16-bit) [cite: 86]
        wf.setframerate(SAMPLE_RATE)
        
        # Transformăm fiecare valoare din float în întreg pe 16 biți
        for sample in wave_data:
            # Scalare la int16 [cite: 206]
            value = int(sample * 32767)
            # Împachetăm valoarea în format binar
            wf.writeframesraw(struct.pack('<h', value))

# --- Rulare ---
midi_notes = [48, 50, 52, 53, 55, 69, 71, 72]
note_names = ["C3", "D3", "E3", "F3", "G3", "A4", "B4", "C4"]

for i, midi in enumerate(midi_notes):
    freq = midi_to_frequency(midi)
    print(f"Nota {note_names[i]}: {freq:.2f} Hz")
    
    wave_data = generate_sine_wave(freq, 0.5)
    filename = f"{note_names[i]}.wav"
    
    save_wave_nativ(filename, wave_data)
    print(f"Am salvat {filename}")
    
    # Redare folosind winsound (FĂRĂ PYGAME)
    winsound.PlaySound(filename, winsound.SND_FILENAME)