```python
import numpy as np
import cv2 as cv

# Cargar el clasificador Haar preentrenado para detectar rostros
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Cargar la máscara
mask = cv.imread("C:/Users/leoda/Documents/Mascara.png", -1)

# Función para superponer la máscara en la cara
def overlay_mask(frame, mask, x, y, w, h):
    # Ajustar el factor de escala para el ancho y el alto de la máscara
    scale_factor_width = 1.2  # Factor de escala para el ancho
    scale_factor_height = 1.5  # Factor de escala para la altura

    mask_width = int(w * scale_factor_width)  # Ajustar el ancho de la máscara en función del ancho del rostro
    mask_height = int(h * scale_factor_height)  # Ajustar la altura de la máscara en función del alto del rostro

    # Redimensionar la máscara dinámicamente al tamaño calculado
    mask_resized = cv.resize(mask, (mask_width, mask_height))

    # Centrar la máscara en el rostro detectado
    mask_x = x + w // 2 - mask_width // 2  # Centrar horizontalmente
    mask_y = y + h // 2 - mask_height // 2  # Centrar verticalmente

    # Superponer la máscara
    for i in range(mask_resized.shape[0]):
        for j in range(mask_resized.shape[1]):
            if mask_resized[i, j][3] != 0:  # Si el pixel no es transparente
                if 0 <= mask_y + i < frame.shape[0] and 0 <= mask_x + j < frame.shape[1]:
                    frame[mask_y + i, mask_x + j] = mask_resized[i, j][:3]  # Superponer la máscara


# Iniciar captura de video
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  # Convertir a escala de grises
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)  # Detectar rostros

    for (x, y, w, h) in faces:
        # Superponer la máscara redimensionable, basada en el tamaño del rostro
        overlay_mask(frame, mask, x, y, w, h)

        # Solo procesar el primer rostro detectado
        break

    # Mostrar el frame con la máscara aplicada
    cv.imshow('Filtro de máscara redimensionable', frame)

    # Si se presiona la tecla 'Esc', salir del bucle
    if cv.waitKey(1) & 0xFF == 27:
        break

# Liberar la cámara y cerrar las ventanas
cap.release()
cv.destroyAllWindows()
```