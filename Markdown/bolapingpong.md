```python
import cv2
import numpy as np

# Dimensiones de la ventana
window_width = 600
window_height = 500

# Parámetros de la pelota de colores
ball_radius = 20
ball_x = window_width // 2
ball_y = window_height // 2
ball_speed_x = 3  # Velocidad en el eje x
ball_speed_y = 3  # Velocidad en el eje y
ball_color = (244, 9, 0)  # Color inicial de la pelota de colores

# Parámetros de la pelota negra
black_ball_radius = 30
black_ball_x = np.random.randint(black_ball_radius, window_width - black_ball_radius)
black_ball_y = np.random.randint(black_ball_radius, window_height - black_ball_radius)
black_ball_speed_x = 4  # Velocidad en el eje x
black_ball_speed_y = 4  # Velocidad en el eje y
black_ball_color = (0, 0, 0)  # Pelota negra

# Función para generar un color aleatorio
def generar_color_aleatorio():
    return tuple(np.random.randint(0, 256, size=3).tolist())

# Crear una ventana
cv2.namedWindow("Pelota rebotando")

# Bucle principal
while True:
    # Crear una imagen blanca (lienzo)
    img = np.ones((window_height, window_width, 3), dtype=np.uint8) * 255

    # Actualizar la posición de la pelota de colores
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Verificar si la pelota de colores toca los bordes y cambiar dirección y color
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= window_width:
        ball_speed_x *= -1  # Cambiar la dirección en el eje x
        ball_color = generar_color_aleatorio()  # Cambiar color
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= window_height:
        ball_speed_y *= -1  # Cambiar la dirección en el eje y
        ball_color = generar_color_aleatorio()  # Cambiar color

    # Actualizar la posición de la pelota negra para esquivar la de colores
    # Si la pelota negra está demasiado cerca de la pelota de colores, cambiar dirección
    distance_x = ball_x - black_ball_x
    distance_y = ball_y - black_ball_y
    distance = np.sqrt(distance_x**2 + distance_y**2)

    if distance < (ball_radius + black_ball_radius + 50):  # Si la distancia es pequeña, esquivar
        if distance_x > 0:
            black_ball_x -= black_ball_speed_x  # Moverse en la dirección opuesta al eje x
        else:
            black_ball_x += black_ball_speed_x
        if distance_y > 0:
            black_ball_y -= black_ball_speed_y  # Moverse en la dirección opuesta al eje y
        else:
            black_ball_y += black_ball_speed_y

    # Verificar si la pelota negra toca los bordes y cambiar dirección
    if black_ball_x - black_ball_radius <= 0:
        black_ball_x = black_ball_radius  # Mantener dentro del límite izquierdo
        black_ball_speed_x *= -1  # Cambiar la dirección en el eje x
    elif black_ball_x + black_ball_radius >= window_width:
        black_ball_x = window_width - black_ball_radius  # Mantener dentro del límite derecho
        black_ball_speed_x *= -1  # Cambiar la dirección en el eje x

    if black_ball_y - black_ball_radius <= 0:
        black_ball_y = black_ball_radius  # Mantener dentro del límite superior
        black_ball_speed_y *= -1  # Cambiar la dirección en el eje y
    elif black_ball_y + black_ball_radius >= window_height:
        black_ball_y = window_height - black_ball_radius  # Mantener dentro del límite inferior
        black_ball_speed_y *= -1  # Cambiar la dirección en el eje y

    # Dibujar la pelota de colores
    cv2.circle(img, (ball_x, ball_y), ball_radius, ball_color, -1)

    # Dibujar la pelota negra
    cv2.circle(img, (black_ball_x, black_ball_y), black_ball_radius, black_ball_color, -1)

    # Dibujar la carita triste ":c" sobre la pelota negra
    # Ojos
    eye_radius = 3
    eye_color = (255, 255, 255)  # Color blanco para los ojos
    cv2.circle(img, (black_ball_x - 5, black_ball_y - 5), eye_radius, eye_color, -1)  # Ojo izquierdo
    cv2.circle(img, (black_ball_x + 5, black_ball_y - 5), eye_radius, eye_color, -1)  # Ojo derecho

    # Boca triste ":c"
    mouth_color = (255, 255, 255)  # Color blanco para la boca
    cv2.ellipse(img, (black_ball_x, black_ball_y + 5), (8, 4), 0, 180, 360, mouth_color, 2)  # Boca triste invertida

    # Mostrar la imagen
    cv2.imshow("Pelota rebotando", img)

    # Controlar la velocidad de fotogramas (esperar 10 ms)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break  # Presiona 'q' para salir

# Cerrar la ventana
cv2.destroyAllWindows()

```