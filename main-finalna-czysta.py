import cv2
import numpy as np
import moviepy.editor as mp

# === USTAWIENIA (WERSJA FINALNA) ===
# Ścieżki do plików
input_path = r"C:\Users\karos\OneDrive\Pulpit\firma-webszyk\klienci\miodek\recenzja.mp4"
output_path = r"C:\Users\karos\OneDrive\Pulpit\firma-webszyk\klienci\miodek\recenzja_finalna_czysta.mp4"

# Parametry do regulacji
KONTRAST_CLIP_LIMIT = 1.2  # Ten parametr już lubisz, kontroluje kontrast.
SIŁA_WYOSTRZANIA = 4.8  # NOWY PARAMETR! Oryginalnie było 5.0.


# Zmniejsz, aby osłabić wyostrzanie i zredukować ziarno (np. 4.7).
# Zwiększ, jeśli chcesz mocniejszą ostrość (np. 5.1).

# Funkcja poprawiająca jakość pojedynczej klatki (szybka wersja)
def enhance_frame(frame):
    # Konwersja z RGB (moviepy) na BGR (OpenCV)
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Krok 1: Poprawa kontrastu w przestrzeni LAB (z łagodniejszymi ustawieniami)
    lab = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=KONTRAST_CLIP_LIMIT, tileGridSize=(8, 8))
    l_enhanced = clahe.apply(l)

    lab_enhanced = cv2.merge((l_enhanced, a, b))
    frame_contrast = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)

    # Krok 2: Subtelne wyostrzenie (z regulowaną siłą)
    # Zamiast "5" używamy teraz parametru SIŁA_WYOSTRZANIA
    kernel = np.array([[0, -1, 0],
                       [-1, SIŁA_WYOSTRZANIA, -1],
                       [0, -1, 0]])
    frame_sharp = cv2.filter2D(frame_contrast, -1, kernel)

    # Konwersja z powrotem do RGB dla moviepy
    return cv2.cvtColor(frame_sharp, cv2.COLOR_BGR2RGB)


# --- Główna część skryptu ---
if __name__ == "__main__":
    clip = mp.VideoFileClip(input_path)

    print("Rozpoczynam przetwarzanie wideo (udoskonalona szybka wersja)...")
    enhanced_clip = clip.fl_image(enhance_frame)

    print("Zapisywanie pliku wideo...")
    enhanced_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    print(f"\nGotowe! Plik zapisano jako: {output_path}")