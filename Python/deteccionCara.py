import numpy as np
import cv2 as cv

# Usar el clasificador Haar preentrenado para detectar rostros y ojos
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_eye.xml')

cap = cv.VideoCapture(0)

# Tamaño constante de las bolas blancas (ojos) y la pupila
eye_radius = 20  # Tamaño del ojo (blanco)
pupil_radius = 8  # Tamaño de la pupila (negro)

while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  # Convierte la imagen a escala de grises
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)  # Detectar rostros

    for (x, y, w, h) in faces:
        # Dibuja un rectángulo alrededor del rostro
        frame = cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Definir la región de interés (ROI) para los ojos, dentro del área del rostro
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # Detectar ojos dentro de la región del rostro
        eyes = eye_cascade.detectMultiScale(roi_gray)

        # Añadir bolas blancas y negras para cada ojo detectado
        for (ex, ey, ew, eh) in eyes:
            # Coordenadas del centro de cada ojo
            center_x = int(ex + ew / 2)
            center_y = int(ey + eh / 2)

            # Dibuja una bola blanca (simulando la parte blanca del ojo)
            cv.circle(roi_color, (center_x, center_y), eye_radius, (255, 255, 255), -1)  # Blanco

            # Dibuja un círculo negro más pequeño en el centro (simulando la pupila)
            cv.circle(roi_color, (center_x, center_y), pupil_radius, (0, 0, 0), -1)  # Negro

        # Dibujar la boca como un óvalo debajo de los ojos
        # La boca se colocará aproximadamente en el centro inferior del rostro
        mouth_center_x = int(w / 2)  # Centro de la boca a la mitad del ancho del rostro
        mouth_center_y = int(h * 0.75)  # Boca 3/4 hacia abajo del rostro
        mouth_width = int(w * 0.4)  # Ancho de la boca (40% del ancho del rostro)
        mouth_height = int(h * 0.1)  # Altura de la boca (10% de la altura del rostro)

        # Dibuja un óvalo rojo para la boca
        cv.ellipse(roi_color, (mouth_center_x, mouth_center_y), (mouth_width, mouth_height), 0, 0, 360, (0, 0, 255), -1)

        # Solo procesar el primer rostro detectado
        break

    # Mostrar el frame con el filtro aplicado
    cv.imshow('Filtro de ojos y boca', frame)

    # Si se presiona la tecla 'Esc', salir del bucle
    if cv.waitKey(1) & 0xFF == 27:
        break

# Libera la cámara y cierra las ventanas
cap.release()
cv.destroyAllWindows()
