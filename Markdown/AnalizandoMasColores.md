```python
import cv2 
import numpy as np 

# Leer la imagen en formato RGB
imagen = cv2.imread('man1.jpeg', 1)

# Convertir la imagen de RGB a HSV
imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

# Definir el rango de color rojo en HSV
bajo_rojo1 = np.array([0, 40, 40])
alto_rojo1 = np.array([10, 255, 255])
bajo_rojo2 = np.array([160, 40, 40])
alto_rojo2 = np.array([180, 255, 255])

# Crear una máscara para el color rojo
mascara_rojo1 = cv2.inRange(imagen_hsv, bajo_rojo1, alto_rojo1)
mascara_rojo2 = cv2.inRange(imagen_hsv, bajo_rojo2, alto_rojo2)
mascara_rojo = cv2.add(mascara_rojo1, mascara_rojo2)

# Convertir la imagen original a escala de grises
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Convertir la imagen gris a un formato BGR para que coincida con la original
imagen_gris_bgr = cv2.cvtColor(imagen_gris, cv2.COLOR_GRAY2BGR)

# Combinar la imagen en gris con las áreas en rojo
resultado = np.where(mascara_rojo[:, :, None] == 255, imagen, imagen_gris_bgr)

# Mostrar la imagen final
cv2.imshow('Color resaltado', resultado)
cv2.waitKey(0)
cv2.destroyAllWindows()
```