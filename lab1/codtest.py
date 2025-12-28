import wave
import numpy as np
import matplotlib.pyplot as plt
import winsound
import os

# 1. Funcție pentru citire metadate
def get_wav_details(file_path):
    with wave.open(file_path, mode='rb') as wf:
        channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        frame_rate = wf.getframerate()
        num_frames = wf.getnframes()
        duration = num_frames / frame_rate
        
        print(f"--- Detalii: {os.path.basename(file_path)} ---")
        print(f"Canale: {channels}")
        print(f"Bit Depth: {sample_width * 8} bits")
        print(f"Sample Rate: {frame_rate} Hz")
        print(f"Durată: {duration:.2f} secunde\n")

# 2. Funcție pentru extragere date audio
def get_audio_data(file_path):
    with wave.open(file_path, mode='rb') as wf:
        channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        frame_rate = wf.getframerate()
        num_frames = wf.getnframes()
        
        frames = wf.readframes(num_frames)
        dtype = np.int16 if sample_width == 2 else np.int8
        audio_data = np.frombuffer(frames, dtype=dtype)
        
        return audio_data, channels, frame_rate

# 3. Funcție pentru izolare canal (Mono)
def get_first_channel(data, num_channels):
    if num_channels > 1:
        audio_data = data.reshape(-1, num_channels)
        return audio_data[:, 0]
    return data

# 4. Funcție pentru afișare Waveform
def plot_audio_wave(data, rate, title="Audio Waveform"):
    time = np.linspace(0, len(data) / rate, num=len(data))
    plt.figure(figsize=(12, 4))
    plt.plot(time, data, color="purple", linewidth=0.5)
    plt.title(title)
    plt.xlabel("Timp (secunde)")
    plt.ylabel("Amplitudine")
    plt.grid(True, alpha=0.3)
    plt.show()

# 5. Funcție pentru salvare fișier nou
def save_new_audio(outfile, data, rate, depth=2):
    with wave.open(outfile, mode='wb') as output_wf:
        output_wf.setnchannels(1)
        output_wf.setsampwidth(depth)
        output_wf.setframerate(rate)
        output_wf.writeframes(data.tobytes())

# --- EXEMPLE DE UTILIZARE CU FIȘIERELE TALE ---

# Alege un fișier din lista ta (ex: chitara sau sinusoida)
file_name = "groove-soul-acoustic-guitar-melody_80bpm_D_minor.wav"
# file_name = "sine-wave-440hz-frequency_69bpm_D_minor.wav"

try:
    # Afișăm detaliile
    get_wav_details(file_name)

    # Procesăm datele
    data, channels, rate = get_audio_data(file_name)
    data_mono = get_first_channel(data, channels)

    # Exemplu: Reducem volumul (împărțire la 4)
    data_quiet = (data_mono / 4).astype(np.int16)

    # Afișăm graficul
    plot_audio_wave(data_mono, rate, title=f"Waveform: {file_name}")

    # Salvăm o variantă modificată
    # save_new_audio("output_mono.wav", data_mono, rate)
    
except FileNotFoundError:
    print(f"Eroare: Fișierul '{file_name}' nu a fost găsit în directorul curent.")