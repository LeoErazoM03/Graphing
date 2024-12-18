```python
import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import cv2
import mediapipe as mp
import numpy as np
import math

# Variables globales
rotation_x = 0  # Rotación en el eje X
rotation_y = 0  # Rotación en el eje Y
scale = 1.0     # Escalamiento del cubo
prev_x = 0      # Coordenada X previa para rotación
prev_y = 0      # Coordenada Y previa para rotación
width, height = 640, 480  # Resolución de la ventana

# Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Dibujar el cubo 3D
def draw_cube():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()

    # Aplicar rotación
    glRotatef(rotation_x, 1, 0, 0)  # Rotación en X
    glRotatef(rotation_y, 0, 1, 0)  # Rotación en Y

    # Aplicar escalamiento
    glScalef(scale, scale, scale)

    # Dibujar el cubo
    glBegin(GL_QUADS)

    # Cara frontal (rojo)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)

    # Cara trasera (verde)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)

    # Cara izquierda (azul)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)

    # Cara derecha (amarillo)
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)

    # Cara superior (cyan)
    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, -0.5)

    # Cara inferior (magenta)
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)

    glEnd()
    glPopMatrix()

# Calcular distancia entre dos puntos
def calculate_distance(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

# Actualizar la rotación y el escalamiento del cubo
def update_cube(hand_landmarks):
    global rotation_x, rotation_y, scale, prev_x, prev_y

    if hand_landmarks:
        # Coordenadas de la palma de la mano (landmark 9)
        y = hand_landmarks.landmark[9].y
        x = hand_landmarks.landmark[9].x

        # Rotar el cubo con los movimientos de la mano
        if prev_y:
            rotation_x -= (y - prev_y) * 300  # Ajustar sensibilidad
        if prev_x:
            rotation_y += (prev_x - x) * 350

        # Calcular escalamiento usando landmarks 4 (pulgar) y 8 (índice)
        thumb = hand_landmarks.landmark[4]
        index = hand_landmarks.landmark[8]
        distance = calculate_distance(thumb, index)

        # Escalar el cubo en función de la distancia
        scale = max(0.05, min(1.5, distance * 4))  # Limitar entre 0.5 y 2.0

        prev_y = y
        prev_x = x

# Captura de video con Mediapipe
def capture_video():
    cap = cv2.VideoCapture(0)

    while not glfw.window_should_close(window):
        ret, frame = cap.read()
        if not ret:
            break

        # Procesar frame con Mediapipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Dibujar las manos detectadas en el frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                # Actualizar el cubo según los gestos
                update_cube(hand_landmarks)

        # Mostrar el frame
        cv2.imshow('Video Feed', frame)

        # Salir con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Inicializar GLFW y OpenGL
if not glfw.init():
    raise Exception("GLFW no se pudo inicializar")

window = glfw.create_window(width, height, "Cubo 3D - OpenGL + Mediapipe", None, None)

if not window:
    glfw.terminate()
    raise Exception("No se pudo crear la ventana GLFW")

glfw.make_context_current(window)
glEnable(GL_DEPTH_TEST)  # Habilitar profundidad

# Hilo para captura de video
import threading
video_thread = threading.Thread(target=capture_video)
video_thread.start()

# Bucle principal de renderizado
while not glfw.window_should_close(window):
    glfw.poll_events()
    draw_cube()
    glfw.swap_buffers(window)

glfw.terminate()

```