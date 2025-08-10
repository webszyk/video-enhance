import cv2
import numpy as np
import moviepy.editor as mp

# === USTAWIENIA ===
input_path = r"C:\Users\karos\OneDrive\Pulpit\firma-webszyk\klienci\miodek\recenzja.3.mp4"
output_path = r"C:\Users\karos\OneDrive\Pulpit\firma-webszyk\klienci\miodek\recenzja_ulepszony.mp4"


# Funkcja poprawiająca jakość pojedynczej klatki
def enhance_frame(frame):
    # Konwersja do LAB (dla lepszego kontrastu)
    lab = cv2.cvtColor(frame, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)

    # Delikatne wyrównanie jasności i kontrastu
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)

    lab = cv2.merge((l, a, b))
    frame_enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

    # Subtelne wyostrzenie
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    frame_sharp = cv2.filter2D(frame_enhanced, -1, kernel)

    return frame_sharp

# Wczytanie wideo
clip = mp.VideoFileClip(input_path)

# Przetworzenie całego wideo
enhanced_clip = clip.fl_image(enhance_frame)

# Zapis z zachowaniem oryginalnego FPS i audio
enhanced_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

print(f"Gotowe! Plik zapisano jako: {output_path}")
