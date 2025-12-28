import numpy as np
import wave
import winsound
import struct

# Configurații
SAMPLE_RATE = 44100
A4_FREQ = 440.0

def midi_to_frequency(midi_note):
    """Conversie MIDI la Hz"""
    return A4_FREQ * (2 ** ((midi_note - 69) / 12))

def play_chord(notes, duration=1.5, name="chord"):
    """Generează un acord prin sumarea mai multor unde sinusoidale"""
    total_samples = int(SAMPLE_RATE * duration)
    combined_wave = np.zeros(total_samples)
    
    for midi in notes:
        freq = midi_to_frequency(midi)
        t = np.linspace(0, duration, total_samples, endpoint=False)
        # Sinteză aditivă: adunăm eșantioanele fiecărei note
        combined_wave += 0.2 * np.sin(2 * np.pi * freq * t)
    
    # Normalizare pentru a evita distorsiunea (clipping)
    combined_wave = combined_wave / len(notes)
    
    # Salvare fișier WAV
    filename = f"{name}.wav"
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        for sample in combined_wave:
            value = int(sample * 32767)
            wf.writeframesraw(struct.pack('<h', value))
    
    print(f"Redăm acordul {name} (Note MIDI: {notes})")
    winsound.PlaySound(filename, winsound.SND_FILENAME)

if __name__ == "__main__":
    # Test: Acord Do Major (C4-E4-G4)
    play_chord([60, 64, 67], name="Do_Major")
    
    # Test: Acord La Minor (A3-C4-E4)
    play_chord([57, 60, 64], name="La_Minor")