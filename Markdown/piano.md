```python
import numpy as np
import cv2 as cv
import mediapipe as mp
import simpleaudio as sa
from scipy.io.wavfile import write
import os

# Configuración inicial
width, height = 640, 480

# Generar sonidos y almacenarlos en un diccionario
os.makedirs("sounds", exist_ok=True)

def generate_tone(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    return (wave * 32767).astype(np.int16)

tones = {
    "A": 440.00,  # La
    "B": 493.88,  # Si
    "C": 523.25,  # Do
    "D": 587.33,  # Re
    "E": 659.25,  # Mi
}

sound_objects = {}
for note, freq in tones.items():
    sound_file = f"sounds/{note}.wav"
    if not os.path.exists(sound_file):
        sound = generate_tone(freq, 1)  # Genera 1 segundo de tono
        write(sound_file, 44100, sound)
    sound_objects[note] = sa.WaveObject.from_wave_file(sound_file)

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Configurar la captura de video
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Error al abrir la cámara.")
    exit()

# Asignar sonidos a dedos
finger_notes = {
    mp_hands.HandLandmark.THUMB_TIP: "A",
    mp_hands.HandLandmark.INDEX_FINGER_TIP: "B",
    mp_hands.HandLandmark.MIDDLE_FINGER_TIP: "C",
    mp_hands.HandLandmark.RING_FINGER_TIP: "D",
    mp_hands.HandLandmark.PINKY_TIP: "E",
}

# Estado previo de los dedos
previous_finger_states = {note: False for note in finger_notes.values()}

# Main loop
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al leer el cuadro de la cámara.")
            break

        frame = cv.flip(frame, 1)
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for landmark_id, note in finger_notes.items():
                    if 0 <= landmark_id - 2 < len(hand_landmarks.landmark):
                        lm = hand_landmarks.landmark[landmark_id]
                        base_lm = hand_landmarks.landmark[landmark_id - 2]

                        # Verificar si el dedo está bajado
                        is_finger_down = lm.y > base_lm.y

                        if is_finger_down and not previous_finger_states[note]:
                            print(f"Reproduciendo {note}")
                            try:
                                play_obj = sound_objects[note].play()
                                # No esperamos que termine para permitir múltiples sonidos
                            except Exception as e:
                                print(f"Error al reproducir {note}: {e}")
                            previous_finger_states[note] = True
                        elif not is_finger_down:
                            previous_finger_states[note] = False

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv.imshow("Detección de dedos", frame)

        if cv.waitKey(10) & 0xFF == 27:  # Salir con ESC
            break

except KeyboardInterrupt:
    print("Interrupción del usuario.")

finally:
    # Limpiar recursos
    cap.release()
    cv.destroyAllWindows()

```