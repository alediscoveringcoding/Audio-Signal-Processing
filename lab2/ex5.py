import tkinter as tk
import numpy as np
import wave
import winsound
import struct
import os

# Configurații Audio
SAMPLE_RATE = 44100
A4_FREQ = 440.0

def midi_to_frequency(midi_note):
    """Transformă nota MIDI în frecvență Hertz"""
    return A4_FREQ * (2 ** ((midi_note - 69) / 12))

def save_and_play_note(midi_note, name):
    """Generează, salvează și redă o notă individuală"""
    filename = f"note_{name}.wav"
    
    # Generăm fișierul doar dacă nu există deja pentru a economisi timp
    if not os.path.exists(filename):
        duration = 0.5
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        freq = midi_to_frequency(midi_note)
        # Amplitudine de 0.3 pentru un sunet clar
        wave_data = 0.3 * np.sin(2 * np.pi * freq * t)
        
        # Salvare binară în format WAV (16-bit PCM)
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 2 bytes (16 biți)
            wf.setframerate(SAMPLE_RATE)
            for sample in wave_data:
                wf.writeframesraw(struct.pack('<h', int(sample * 32767)))
    
    # Redare ASYNC pentru a nu bloca interfața grafică
    winsound.PlaySound(filename, winsound.SND_FILENAME | winsound.SND_ASYNC)

# Configurare Interfață Grafică
root = tk.Tk()
root.title("Piano App - PSA")

# Notele albe: C4 (Do), D4, E4, F4, G4, A4, B4, C5
white_notes = [
    ("C", 60), ("D", 62), ("E", 64), ("F", 65),
    ("G", 67), ("A", 69), ("B", 71), ("C2", 72)
]

print("Pianul este activ. Apasă tastele din fereastră!")

# Generare butoane în interfață
for i, (name, midi) in enumerate(white_notes):
    btn = tk.Button(
        root, 
        text=name, 
        width=6, 
        height=12, 
        bg="white", 
        font=("Arial", 10, "bold"),
        command=lambda m=midi, n=name: save_and_play_note(m, n)
    )
    btn.grid(row=0, column=i, padx=2, pady=10)

root.mainloop()