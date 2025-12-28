import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy.fftpack as fft

# --- EXERCIȚIUL 1 & 2: Analiză Acord DO Major ---
def analiza_acord_major(file_path):
    sample_rate, data = wavfile.read(file_path)
    n = len(data)
    
    # Calculăm Transformata Fourier Reală (RFFT)
    frequencies = np.fft.rfftfreq(n, d=1/sample_rate)
    fft_values = np.fft.rfft(data)
    magnitudes = np.abs(fft_values)
    
    # Identificăm cele mai dominante 3 frecvențe
    N = 3
    sorted_indices = np.argsort(-magnitudes)
    dominant_frequencies = frequencies[sorted_indices[:N]]
    dominant_magnitudes = magnitudes[sorted_indices[:N]]
    
    print(f"Frecvențe dominante: {dominant_frequencies}")

    # Plotare Rezultate
    plt.figure(figsize=(12, 10))
    
    # Semnalul original (primul 1000 de eșantioane)
    plt.subplot(3, 1, 1)
    plt.plot(data[:1000], color='blue')
    plt.title("Acordul DO Major - Semnal în Timp")
    plt.xlabel("Eșantioane")
    plt.ylabel("Amplitudine")

    # Spectrul de frecvență
    plt.subplot(3, 1, 2)
    plt.plot(frequencies, magnitudes, color='blue')
    plt.title("Spectru frecvențe pentru acordul DO Major")
    plt.xlabel("Frecventa (Hz)")
    plt.ylabel("Magnitudinea")
    plt.xlim(0, 500)
    plt.grid(True)
    
    # --- EXERCIȚIUL 3: Descompunerea în note muzicale ---
    plt.subplot(3, 1, 3)
    time = np.linspace(0, 1, sample_rate)
    for freq, mag in zip(dominant_frequencies, dominant_magnitudes):
        # Recreăm unda sinusoidală pentru fiecare frecvență dominantă
        sine_wave = mag * np.sin(2 * np.pi * freq * time)
        plt.plot(time[:1000], sine_wave[:1000], label=f"{freq:.2f} Hz")
    
    plt.title("Forma de undă a notelor muzicale individuale")
    plt.xlabel("Timp (s)")
    plt.ylabel("Amplitudine")
    plt.legend()
    plt.tight_layout()
    plt.show()

# --- EXERCIȚIUL 4: Curățare Zgomot ---
def curatare_zgomot(input_file):
    sample_rate, noisy_signal = wavfile.read(input_file)
    n_samples = len(noisy_signal)
    
    # Trecem în domeniul frecvență
    noisy_signal_fft = np.fft.fft(noisy_signal)
    frequencies = np.fft.fftfreq(n_samples, 1/sample_rate)
    
    # Filtrare: eliminăm frecvențele peste 5000 Hz
    noise_threshold = 5000
    filtered_fft = noisy_signal_fft.copy()
    filtered_fft[np.abs(frequencies) > noise_threshold] = 0
    
    # Transformata inversă pentru a reveni în domeniul timp
    cleaned_signal = np.real(np.fft.ifft(filtered_fft))
    
    # Salvare fișier curățat
    wavfile.write("cleaned_output.wav", sample_rate, cleaned_signal.astype(np.int16))
    
    # Vizualizare
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(noisy_signal[:1000])
    plt.title("Semnal cu zgomot")
    
    plt.subplot(2, 1, 2)
    plt.plot(cleaned_signal[:1000])
    plt.title("Semnal curățat de zgomot")
    plt.tight_layout()
    plt.show()

# --- EXERCIȚIUL 5: Egalizator Audio ---
def egalizator_audio(file_path):
    sample_rate, audio_data = wavfile.read(file_path)
    fft_audio = fft.fft(audio_data)
    frequencies = np.fft.fftfreq(len(audio_data), d=1/sample_rate)
    
    # Vizualizare înainte de filtrare
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.plot(frequencies[:len(frequencies)//2], np.abs(fft_audio)[:len(frequencies)//2])
    plt.title('Original (Spectrograma înainte de filtrare)')
    plt.ylabel('Magnitudine')
    
    # Aplicare filtru (ex: tăiem frecvențele joase sub 1000Hz)
    fft_audio[np.abs(frequencies) < 1000] = 0
    
    # Reconstrucție
    filtered_audio = np.real(fft.ifft(fft_audio))
    wavfile.write('output_filtered.wav', sample_rate, np.int16(filtered_audio))
    
    # Vizualizare după filtrare
    plt.subplot(2, 1, 2)
    plt.plot(frequencies[:len(frequencies)//2], np.abs(fft_audio)[:len(frequencies)//2])
    plt.title('Spectru frecvențial după modificări')
    plt.xlabel('Frecventa (Hz)')
    plt.ylabel('Magnitudine')
    plt.tight_layout()
    plt.show()

# Apelarea funcțiilor (Asigură-te că fișierele există pe disc)
analiza_acord_major('chord_C_major.wav')  # Execută analiza acordului [cite: 7, 11]
curatare_zgomot('extracted_channel_out.wav') # Execută eliminarea zgomotului [cite: 103, 104]
egalizator_audio('bad-guy.wav') # Execută egalizatorul audio [cite: 123, 132]