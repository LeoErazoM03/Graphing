import cv2 as cv
import numpy as np

# Cargar la imagen en escala de grises
img = cv.imread('C:\\Users\\leoda\\OneDrive\\-\\Instituto\\Tecnológico\\de\\Morelia\\Web Desing\\Graficación\\caballo.jpeg', 0)

# Obtener el tamaño de la imagen
x, y = img.shape

# Calcular el centro de la imagen
center = (y // 2, x // 2)

# Definir el ángulo de rotación (en grados)
angle = 45

# Crear la matriz de rotación
M = cv.getRotationMatrix2D(center, angle, 1.0)

# Aplicar la rotación usando warpAffine
rotated_img = cv.warpAffine(img, M, (y, x))

# Mostrar la imagen original y la rotada
cv.imshow('Imagen Original', img)
cv.imshow('Imagen Rotada', rotated_img)
cv.waitKey(0)
cv.destroyAllWindows()