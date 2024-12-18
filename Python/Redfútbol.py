import numpy as np
import cv2 as cv

# Configuración inicial
width, height = 640, 480  # Tamaño de la ventana
rows, cols = 2, 2  # Tamaño de la cuadrícula
ball_radius = 15  # Radio de la pelota
ball_color = (0, 0, 255)  # Color de la pelota (rojo en BGR)
speed_factor = 3.0  # Factor de velocidad para el movimiento de la pelota

# Crear la cuadrícula inicial de puntos
x_spacing = width // (cols + 1)
y_spacing = height // (rows + 1)
points = np.array([[[(j + 1) * x_spacing, (i + 1) * y_spacing]] for i in range(rows) for j in range(cols)], dtype=np.float32)

# Posición inicial de la pelota
ball_position = np.array([width // 2, height // 2], dtype=np.float32)

# Configurar la captura de video
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Error al abrir la cámara.")
    exit()

# Leer el primer cuadro para el cálculo de movimiento
ret, prev_frame = cap.read()
if not ret:
    print("Error al leer el cuadro inicial.")
    cap.release()
    exit()
prev_gray = cv.cvtColor(prev_frame, cv.COLOR_BGR2GRAY)

# Función para calcular el movimiento promedio de la cuadrícula
def calculate_average_motion(points, motion_mask):
    motion_vectors = []
    for point in points:
        x, y = point.ravel()
        if 0 <= x < width and 0 <= y < height and motion_mask[int(y), int(x)] > 0:
            motion_vectors.append([np.random.uniform(-10, 10), np.random.uniform(-10, 10)])

    if motion_vectors:
        avg_motion = np.mean(motion_vectors, axis=0)
    else:
        avg_motion = np.array([0, 0])

    return avg_motion

# Función para dibujar la cuadrícula
def draw_grid(frame, points):
    for point in points:
        x, y = point.ravel()
        cv.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)  # Dibuja los puntos

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al leer el cuadro de la cámara.")
        break

    # Convertir el cuadro actual a escala de grises
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Calcular la diferencia de movimiento
    diff = cv.absdiff(prev_gray, gray)
    _, motion_mask = cv.threshold(diff, 30, 255, cv.THRESH_BINARY)

    # Calcular el movimiento promedio
    avg_motion = calculate_average_motion(points, motion_mask)

    # Actualizar la posición de la pelota
    ball_position += avg_motion * speed_factor

    # Restringir la posición de la pelota dentro de los límites de la ventana
    ball_position[0] = np.clip(ball_position[0], ball_radius, width - ball_radius)
    ball_position[1] = np.clip(ball_position[1], ball_radius, height - ball_radius)

    # Dibujar la cuadrícula y la pelota
    output = frame.copy()
    draw_grid(output, points)
    cv.circle(output, (int(ball_position[0]), int(ball_position[1])), ball_radius, ball_color, -1)

    # Mostrar el resultado
    cv.imshow("Ball Control", output)

    # Actualizar el cuadro previo
    prev_gray = gray.copy()

    key = cv.waitKey(10) & 0xFF
    if key == 27:  # Salir con ESC
        break

cap.release()
cv.destroyAllWindows()
