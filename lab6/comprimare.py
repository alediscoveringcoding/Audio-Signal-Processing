import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os
from pydub import AudioSegment

# --- EXERCIȚIUL 1: Metrici de bază ---
def calculate_compression_ratio(original_file, compressed_file):
    original_size = os.path.getsize(original_file)
    compressed_size = os.path.getsize(compressed_file)
    return original_size / compressed_size

def calculate_mse(original, compressed):
    original = np.array(original)
    compressed = np.array(compressed)
    # Ne asigurăm că ambele semnale au aceeași lungime pentru calcul
    min_len = min(len(original), len(compressed))
    return np.mean((original[:min_len] - compressed[:min_len])**2)

# --- EXERCIȚIUL 2: Lossy Compression (Reducerea preciziei) ---
def lossy_compression(signal, precision):
    # Comprimare prin rotunjire la numărul de zecimale dorit
    return [round(sample, precision) for sample in signal]

def plot_compressed_waves(original_wave, compressed_wave):
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.title("Original")
    plt.plot(original_wave[:1000])
    plt.subplot(2, 1, 2)
    plt.title("Comprimat")
    plt.plot(compressed_wave[:1000], color='orange')
    plt.tight_layout()
    plt.show()

# --- EXERCIȚIUL 3: Bit Depth Compression (Fix pentru ValueError 'int8') ---
def bit_depth_compression(input_file):
    sr, data = wavfile.read(input_file)
    
    # Normalizăm datele între -32768 și 32767 pentru formatul int16
    # Am schimbat din int8 în int16 pentru a evita eroarea "Unsupported data type"
    audio_normalized = (data / np.max(np.abs(data))) * 32767
    audio_int16 = audio_normalized.astype(np.int16)
    
    output_file = "output_compressed.wav"
    wavfile.write(output_file, sr, audio_int16)
    
    ratio = calculate_compression_ratio(input_file, output_file)
    mse = calculate_mse(data, audio_int16)
    
    print(f"Raport Compresie (Bit Depth): {ratio:.2f}")
    print(f"MSE: {mse:.6f}")
    return data, audio_int16

# --- EXERCIȚIUL 4: RLE (Run-Length Encoding) ---
def run_length_encode(data):
    if len(data) == 0: return []
    encoded = []
    prev = data[0]
    count = 1
    for val in data[1:]:
        if val == prev:
            count += 1
        else:
            encoded.append((prev, count))
            prev = val
            count = 1
    encoded.append((prev, count))
    return encoded

# --- EXERCIȚIUL 5: MP3 ---
def convert_to_mp3(input_wav, output_mp3):
    audio = AudioSegment.from_wav(input_wav)
    audio.export(output_mp3, format="mp3")
    
    ratio = calculate_compression_ratio(input_wav, output_mp3)
    print(f"Raport Compresie MP3: {ratio:.2f}")

# --- RULARE ---
if __name__ == "__main__":
    file_wav = "input.wav"
    
    if os.path.exists(file_wav):
        # 1. Test Bit Depth
        orig_data, comp_data = bit_depth_compression(file_wav)
        plot_compressed_waves(orig_data, comp_data)
        
        # 2. Test RLE (pe primele 50 eșantioane pentru viteză)
        rle_result = run_length_encode(comp_data[:50])
        print(f"RLE Encoded: {rle_result}")
        
        # 3. Test MP3
        # convert_to_mp3(file_wav, "output.mp3")
    else:
        print(f"Te rog pune fisierul {file_wav} în folderul de lucru!")