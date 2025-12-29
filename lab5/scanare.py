import numpy as np
import matplotlib.pyplot as plt

# Parametrii dați în laborator
f_esantionare = 50e6  # 50 MHz 
viteza_sunet = 1500   # 1500 m/s în apă 

try:
    # Citim datele trimise (asigură-te că fișierul se numește exact A_SCAN.txt)
    with open("ASCAN.txt", "r") as file:
        data = file.read()
    
    # Transformăm textul în numere
    y_values = np.array([float(value) for value in data.strip().split("\n")])
    x_values = np.arange(len(y_values))

    # Identificăm automat vârfurile (Initial Pulse și Defect)
    idx_initial = np.argmax(y_values[:100]) # Primul vârf (impulsul de start)
    idx_defect = np.argmax(y_values[200:]) + 200 # Al doilea vârf (defectul)

    print(f"Vârf Inițial la indexul: {idx_initial}")
    print(f"Vârf Defect la indexul: {idx_defect}")

    # Plotare
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, label="Semnal Ultrasunete")
    plt.axvline(x=idx_initial, color='r', linestyle='--', label="Impuls Inițial")
    plt.axvline(x=idx_defect, color='g', linestyle='--', label="Ecou Defect")
    plt.title("Analiză NDT - A-SCAN")
    plt.xlabel("Index (Eșantioane)")
    plt.ylabel("Amplitudine")
    plt.legend()
    plt.grid(True)
    plt.show()

except Exception as e:
    print(f"Eroare: {e}")