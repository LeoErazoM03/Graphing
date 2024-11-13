import cv2
import numpy as np


def suavizar_imagen(imagen):
    # Obtener las dimensiones de la imagen
    altura, ancho, _ = imagen.shape

    # Crear una nueva imagen para el resultado
    imagen_suavizada = np.zeros((altura, ancho, 3), dtype=np.uint8)

    # Aplicar suavizado pixel por pixel
    for y in range(altura):
        for x in range(ancho):
            suma_r, suma_g, suma_b = 0, 0, 0
            contador = 0

            # Definir los vecinos (izquierda, derecha, arriba, abajo)
            vecinos = [
                (y, x),  # el propio pixel
                (y - 1, x),  # arriba
                (y + 1, x),  # abajo
                (y, x - 1),  # izquierda
                (y, x + 1)  # derecha
            ]

            for vy, vx in vecinos:
                if 0 <= vy < altura and 0 <= vx < ancho:  # Verificar límites
                    pixel = imagen[vy, vx]
                    suma_b += pixel[0]  # Valor B
                    suma_g += pixel[1]  # Valor G
                    suma_r += pixel[2]  # Valor R
                    contador += 1

            # Calcular el nuevo valor promedio para el pixel
            nuevo_b = int(suma_b / contador)
            nuevo_g = int(suma_g / contador)
            nuevo_r = int(suma_r / contador)

            # Asignar los nuevos valores a la imagen suavizada
            imagen_suavizada[y, x] = [nuevo_b, nuevo_g, nuevo_r]

    return imagen_suavizada


def mostrar_imagen_y_suavizar(imagen_path):
    # Cargar la imagen
    imagen = cv2.imread(imagen_path)

    if imagen is None:
        print("Error: No se pudo cargar la imagen. Verifica la ruta.")
        return

    # Suavizar la imagen
    imagen_suavizada = suavizar_imagen(imagen)

    # Mostrar la imagen original y la imagen suavizada
    cv2.imshow("Imagen Original", imagen)
    cv2.imshow("Imagen Suavizada", imagen_suavizada)

    # Esperar a que se presione una tecla
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Ruta de la imagen que deseas cargar
imagen_path = r"C:\Users\leoda\Downloads\perrito.jpg"
mostrar_imagen_y_suavizar(imagen_path)
