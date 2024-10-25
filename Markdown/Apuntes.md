```python
import cv2 as cv  # Importa la librería OpenCV, que se usa para el procesamiento de imágenes y videos.

# Lee una imagen desde el archivo 'tr.png'. 
# El segundo argumento '1' indica que se leerá la imagen en color (1 para color, 0 para escala de grises, -1 para incluir el canal alfa si existe).
img = cv.imread('C:/Users/leoda/OneDrive/-/Instituto/Tecnológico/de/Morelia/Web/Desing/pixel/Ejemplo.png', 1)

# Muestra la imagen leída en una ventana llamada 'ejemplo'.
cv.imshow('ejemplo', img)

# Espera indefinidamente hasta que el usuario presione una tecla.
cv.waitKey(0)

# Cierra todas las ventanas abiertas por OpenCV.
cv.destroyAllWindows() 



```