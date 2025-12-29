import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# --- EXERCIȚIUL 1: Vizualizare Formă de Undă (Waveshow) ---
def exercitiu_1_waveshow(file_path):
    # Încărcăm fișierul folosind librosa [cite: 199]
    samples, sample_rate = librosa.load(file_path, sr=None)
    
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(samples, sr=sample_rate) # [cite: 200]
    plt.title(f"Waveshow: {file_path}")
    plt.show()

# --- EXERCIȚIUL 2: Spectogramă STFT (Linear vs Log) ---
def exercitiu_2_stft(file_path):
    samples, sample_rate = librosa.load(file_path, sr=None)
    
    # Calculăm Short-Time Fourier Transform (STFT) 
    sgram = librosa.stft(samples)
    sgram_db = librosa.amplitude_to_db(np.abs(sgram)) # Conversie în decibeli
    
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 8), sharex=True)
    
    # Spectograma pe axă liniară 
    img1 = librosa.display.specshow(sgram_db, x_axis='time', y_axis='linear', ax=ax[0])
    ax[0].set_title('Spectogramă Liniară (Hz)')
    
    # Spectograma pe axă logaritmică 
    img2 = librosa.display.specshow(sgram_db, x_axis='time', y_axis='log', ax=ax[1])
    ax[1].set_title('Spectogramă Logaritmică (Hz)')
    
    fig.colorbar(img1, ax=ax, format="%+2.f dB") # 
    plt.tight_layout()
    plt.show()

# --- EXERCIȚIUL 3: Vizualizare sub formă de Note Muzicale ---
def exercitiu_3_note(file_path):
    samples, sample_rate = librosa.load(file_path, sr=None)
    sgram = librosa.stft(samples)
    sgram_db = librosa.amplitude_to_db(np.abs(sgram))
    
    plt.figure(figsize=(10, 6))
    # Folosim y_axis='fft_note' pentru a vedea notele pe portativ [cite: 259]
    img = librosa.display.specshow(sgram_db, x_axis='time', y_axis='fft_note')
    
    # Limităm vizualizarea între octavele 3 și 5 conform laboratorului [cite: 259]
    plt.ylim(librosa.note_to_hz('C3'), librosa.note_to_hz('C5'))
    plt.title(f"Spectrogramă Note: {file_path}")
    plt.colorbar(img, format="%+2.f dB")
    plt.show()

# --- EXERCIȚIUL 4: Spectograma Mel (Scara Mel) ---
def exercitiu_4_mel(file_path):
    samples, sample_rate = librosa.load(file_path, sr=None)
    
    # Calculăm Mel Spectrogram [cite: 327]
    mel_scale_sgram = librosa.feature.melspectrogram(y=samples, sr=sample_rate)
    mel_sgram_db = librosa.amplitude_to_db(mel_scale_sgram, ref=np.max) # [cite: 328]
    
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mel_sgram_db, sr=sample_rate, x_axis='time', y_axis='mel') # [cite: 331]
    plt.title(f"Spectrogramă Mel (Percepția Umană): {file_path}")
    plt.colorbar(format="%+2.0f dB")
    plt.show()

# --- EXERCIȚIUL 5: Analiză Armonici ---
def exercitiu_5_armonici(file_path):
    samples, sample_rate = librosa.load(file_path, sr=None)
    sgram = librosa.stft(samples)
    sgram_db = librosa.amplitude_to_db(np.abs(sgram))
    
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(sgram_db, x_axis='time', y_axis='fft_note')
    plt.title(f"Analiză Armonici: {file_path}")
    plt.colorbar(format="%+2.f dB")
    plt.show()

# --- APELAREA FUNCȚIILOR ---
# Note: Asigură-te că fișierele sunt în folderul 'lab3' conform setărilor tale anterioare.

file_guitar = 'groove-soul-acoustic-guitar-melody_80bpm_D_minor.wav'
exercitiu_1_waveshow(file_guitar)
exercitiu_2_stft(file_guitar)
exercitiu_4_mel(file_guitar)

file_birthday = 'happy_birthday.wav'
exercitiu_3_note(file_birthday)

file_piano = 'single-piano-note-c4_100bpm_C_major.wav'
exercitiu_5_armonici(file_piano)