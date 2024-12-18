```python
from math import cos, sin, pi, radians
from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import sys
import random
import numpy as np
import cv2 as cv
import math


radius = 50.0
theta = 0.0  # Ángulo horizontal de la cámara (azimutal).
phi = 45.0  # Ángulo vertical
camera_target = [0.0, 0.0, 0.0]  # Punto central que la cámara observa.
camera_speed = 0.1  
zoom_speed = 2.0  

# camera_x, camera_y, camera_z = 10, 8, 15
# look_at_x, look_at_y, look_at_z = 0, 0, 0
# speed = 0.5


santa_x, santa_z = -10, -10  # Posición inicial de Santa Claus
santa_direction_x, santa_direction_z = 1, 1  # Dirección del movimiento
window = None


# primer carro
carro_x, carro_z = -7, -7  # Posición inicial del carro
carro_direction_x, carro_direction_z = 1, 1  # Dirección del carro


# camion
camion_x, camion_z = -5, -5 # Posición inicial del carro
camion_direction_x, camion_direction_z = 1, 1  # Dirección del carro





# Generar nieve (500 copos en posiciones aleatorias)
snowflakes = [(random.uniform(-20, 20), random.uniform(5, 15), random.uniform(-20, 20)) for _ in range(500)]
# Lista para almacenar las posiciones de las piedras
stones = []


# Inicialización de OpenCV (Flujo óptico)
cap = cv.VideoCapture(0)  
lkparm = dict( 
    winSize=(15, 15),  # Tamaño de la ventana de búsqueda para detección de movimiento.
    maxLevel=2,  # Niveles de la pirámide para buscar puntos en múltiples escalas.
    criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03)  
)
_, vframe = cap.read()  
height, width = vframe.shape[:2]  

# Crear una malla inicial
grid_x, grid_y = np.meshgrid(
    np.linspace(50, width - 50, 10),  
    np.linspace(50, height - 50, 10)
)
p0 = np.vstack([grid_x.ravel(), grid_y.ravel()]).T.astype(np.float32)  # Combina las coordenadas en una lista de puntos.
p0 = p0[:, np.newaxis, :]  # Ajusta la estructura para que sea compatible con OpenCV.


def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.05, 0.05, 0.2, 1.0)  # Azul oscuro para cielo nocturno (opaco)
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1, .1, 100.0)  # Campo de visión más amplio
    glMatrixMode(GL_MODELVIEW)
    
def spherical_to_cartesian(radius, theta, phi):
    """Convierte coordenadas esféricas (radio, teta, phi) a cartesianas (x, y, z) y restringe la altura."""
    theta_rad = math.radians(theta)  # Convierte theta a radianes.
    phi_rad = math.radians(phi)  # Convierte phi a radianes.
    x = radius * math.sin(phi_rad) * math.cos(theta_rad)  # Calcula la coordenada X.
    y = max(radius * math.cos(phi_rad), 5.0)  # Calcula la coordenada Y, con un mínimo de 5.0 para evitar bajar del plano.
    z = radius * math.sin(phi_rad) * math.sin(theta_rad)  # Calcula la coordenada Z.
    return [x, y, z]  # Devuelve las coordenadas cartesianas.

def draw_ground():
    """Dibuja un plano para representar el suelo"""
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.9, 1.0)  # blanco azulado simula nieve
    glVertex3f(-20, 0, 20)
    glVertex3f(20, 0, 20)
    glVertex3f(20, 0, -20)
    glVertex3f(-20, 0, -20)
    glEnd()
###########################################################################################################
def draw_snowflakes():
    """Dibuja copos de nieve como pequeños cuadrados en posiciones aleatorias."""
    glBegin(GL_QUADS)  # Usamos quads para dibujar copos de nieve cuadrados
    glColor3f(1, 1, 1)  # Color blanco para la nieve
    for x, y, z in snowflakes:
        # Dibujar cada copo como un pequeño cuadrado
        glVertex3f(x - 0.1, y - 0.1, z)  # Esquina inferior izquierda
        glVertex3f(x + 0.1, y - 0.1, z)  # Esquina inferior derecha
        glVertex3f(x + 0.1, y + 0.1, z)  # Esquina superior derecha
        glVertex3f(x - 0.1, y + 0.1, z)  # Esquina superior izquierda
    glEnd()
def update_snowflakes():
    """Actualiza las posiciones de los copos de nieve para simular su caída."""
    global snowflakes
    updated_snowflakes = []
    for x, y, z in snowflakes:
        y -= 0.1  # Desplazar hacia abajo
        if y < 0:  # Si el copo llega al suelo, lo reposiciona arriba
            y = random.uniform(5, 15)
        updated_snowflakes.append((x, y, z))
    snowflakes = updated_snowflakes
################################################################################

def draw_stone(x, y, z, size):
    """Dibuja una piedra como una esfera en una posición dada"""
    glPushMatrix()  # Guardar la matriz actual
    glTranslatef(x, y, z)  # Mover la piedra a la posición especificada
    glColor3f(0.7, 0.8, 1.0)  # Color café para las piedras
    gluSphere(gluNewQuadric(), size, 10, 10)  # Dibuja la esfera (piedra)
    glPopMatrix()  # Restaurar la matriz actual

def draw_street():
    """Dibuja calles con líneas discontinuas amarillas para vía de doble sentido"""
    # Dibujar las calles
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.2, 0.2)  # Gris oscuro para las calles

    # Calle horizontal superior (aumentada la separación)
    glVertex3f(-20, 0.01, -10)
    glVertex3f(20, 0.01, -10)
    glVertex3f(20, 0.01, -6)
    glVertex3f(-20, 0.01, -6)

    # Calle horizontal inferior (aumentada la separación)
    glVertex3f(-20, 0.01, 6)
    glVertex3f(20, 0.01, 6)
    glVertex3f(20, 0.01, 10)
    glVertex3f(-20, 0.01, 10)

    # Calle vertical izquierda (aumentada la separación)
    glVertex3f(-10, 0.01, -20)
    glVertex3f(-6, 0.01, -20)
    glVertex3f(-6, 0.01, 20)
    glVertex3f(-10, 0.01, 20)

    # Calle vertical derecha (aumentada la separación)
    glVertex3f(6, 0.01, -20)
    glVertex3f(10, 0.01, -20)
    glVertex3f(10, 0.01, 20)
    glVertex3f(6, 0.01, 20)
    glEnd()

    # Dibujar líneas discontinuas amarillas en el centro de las calles
    glLineWidth(4)  # Establecer el grosor de la línea
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 0.0)  # Amarillo

    # Líneas discontinuas horizontales (vía de doble sentido)
    for i in range(-20, 20, 4):  # Establecer el paso entre cada línea amarilla
        glVertex3f(i, 0.02, -8)  # Ajustar la posición de las líneas
        glVertex3f(i + 2, 0.02, -8)  # Desplazamiento en x para la discontinuidad

    for i in range(-20, 20, 4):  # Líneas discontinuas para la otra calle horizontal
        glVertex3f(i, 0.02, 8)  # Ajustar la posición de las líneas
        glVertex3f(i + 2, 0.02, 8)  # Desplazamiento en x para la discontinuidad

    # Líneas discontinuas verticales (vía de doble sentido)
    for i in range(-20, 20, 4):  # Establecer el paso entre cada línea amarilla
        glVertex3f(-8, 0.02, i)  # Ajustar la posición de las líneas
        glVertex3f(-8, 0.02, i + 2)  # Desplazamiento en z para la discontinuidad

    for i in range(-20, 20, 4):  # Líneas discontinuas para la otra calle vertical
        glVertex3f(8, 0.02, i)  # Ajustar la posición de las líneas
        glVertex3f(8, 0.02, i + 2)  # Desplazamiento en z para la discontinuidad

    glEnd()

def draw_mountain(x_offset, z_offset):
    """Dibuja una montaña en una posición específica"""
    glPushMatrix()  # Guardar la matriz actual
    glTranslatef(x_offset, 0, z_offset)  # Mover la montaña a la posición especificada
    glColor3f(0.7, 0.8, 1.0)  # Color azul claro para la montaña

    # Dibuja la montaña usando un cono o una pirámide
    glBegin(GL_TRIANGLES)
    # Base de la montaña
    glVertex3f(-5, 0, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(0, 10, 0)  # Pico de la montaña

    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(0, 10, 0)  # Pico de la montaña

    glVertex3f(5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(0, 10, 0)  # Pico de la montaña

    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, -5)
    glVertex3f(0, 10, 0)  # Pico de la montaña
    glEnd()

    glPopMatrix()  # Restaurar la matriz actual

###########################################################################

# Objeto: Persona
def draw_cuerpo():
    """Dibuja el torso de la persona."""
    glColor3f(0.2, 0.5, 0.8)  # Azul para la camisa
    glPushMatrix()
    glTranslatef(0.0, 1, 0.0)  # Posición del torso

    glBegin(GL_QUADS)

    # Frente
    glVertex3f(-0.25, -0.45, 0.15)
    glVertex3f(0.25, -0.45, 0.15)
    glVertex3f(0.25, 0.45, 0.15)
    glVertex3f(-0.25, 0.45, 0.15)

    # Atrás
    glVertex3f(-0.25, -0.35, -0.15)
    glVertex3f(0.25, -0.35, -0.15)
    glVertex3f(0.25, 0.35, -0.15)
    glVertex3f(-0.25, 0.35, -0.15)

    # Izquierda
    glVertex3f(-0.25, -0.35, -0.15)
    glVertex3f(-0.25, -0.35, 0.15)
    glVertex3f(-0.25, 0.35, 0.15)
    glVertex3f(-0.25, 0.35, -0.15)

    # Derecha
    glVertex3f(0.25, -0.35, -0.15)
    glVertex3f(0.25, -0.35, 0.15)
    glVertex3f(0.25, 0.35, 0.15)
    glVertex3f(0.25, 0.35, -0.15)

    # Arriba
    glVertex3f(-0.25, 0.35, -0.15)
    glVertex3f(0.25, 0.35, -0.15)
    glVertex3f(0.25, 0.35, 0.15)
    glVertex3f(-0.25, 0.35, 0.15)

    # Abajo
    glVertex3f(-0.25, -0, -0.15)
    glVertex3f(0.25, -0, -0.15)
    glVertex3f(0.25, -0, 0.15)
    glVertex3f(-0.25, -0, 0.15)

    glEnd()
    glPopMatrix()

def draw_cabeza():
    """Dibuja la cabeza de la persona."""
    glPushMatrix()
    glTranslatef(0.0, 1.65, 0.0)  # Posición de la cabeza
    glColor3f(1.0, 0.8, 0.6)  # Color piel
    quadric = gluNewQuadric()
    gluSphere(quadric, 0.25, 32, 32)  # Cabeza esférica
    glPopMatrix()

def draw_brazo(x_offset):
    """Dibuja un brazo de la persona. x_offset define la posición (izquierdo o derecho)."""
    glColor3f(0.2, 0.5, 0.8)  # Azul para la camisa
    glPushMatrix()
    glTranslatef(x_offset, 1.2, 0.0)  # Posición del brazo

    glBegin(GL_QUADS)

    # Frente
    glVertex3f(-0.1, -0.4, 0.1)
    glVertex3f(0.1, -0.4, 0.1)
    glVertex3f(0.1, 0.25, 0.1)
    glVertex3f(-0.1, 0.25, 0.1)

    # Atrás
    glVertex3f(-0.1, -0.4, -0.1)
    glVertex3f(0.1, -0.4, -0.1)
    glVertex3f(0.1, 0.25, -0.1)
    glVertex3f(-0.1, 0.25, -0.1)

    # Izquierda
    glVertex3f(-0.1, -0.4, -0.1)
    glVertex3f(-0.1, -0.4, 0.1)
    glVertex3f(-0.1, 0.25, 0.1)
    glVertex3f(-0.1, 0.25, -0.1)

    # Derecha
    glVertex3f(0.1, -0.4, -0.1)
    glVertex3f(0.1, -0.4, 0.1)
    glVertex3f(0.1, 0.25, 0.1)
    glVertex3f(0.1, 0.25, -0.1)

    glEnd()
    glPopMatrix()

def draw_pierna(x_offset):
    """Dibuja una pierna de la persona. x_offset define la posición (izquierda o derecha)."""
    glColor3f(0.1, 0.1, 0.4)  # Azul oscuro para los pantalones
    glPushMatrix()
    glTranslatef(x_offset, 0.2, 0.0)  # Posición de la pierna

    glBegin(GL_QUADS)

    # Frente
    glVertex3f(-0.1, -0.3, 0.1)
    glVertex3f(0.1, -0.3, 0.1)
    glVertex3f(0.1, 0.5, 0.1)
    glVertex3f(-0.1, 0.5, 0.1)

    # Atrás
    glVertex3f(-0.1, -0.3, -0.1)
    glVertex3f(0.1, -0.3, -0.1)
    glVertex3f(0.1, 0.5, -0.1)
    glVertex3f(-0.1, 0.5, -0.1)

    # Izquierda
    glVertex3f(-0.1, -0.3, -0.1)
    glVertex3f(-0.1, -0.3, 0.1)
    glVertex3f(-0.1, 0.5, 0.1)
    glVertex3f(-0.1, 0.5, -0.1)

    # Derecha
    glVertex3f(0.1, -0.3, -0.1)
    glVertex3f(0.1, -0.3, 0.1)
    glVertex3f(0.1, 0.5, 0.1)
    glVertex3f(0.1, 0.5, -0.1)

    glEnd()
    glPopMatrix()

def draw_persona():
    """Dibuja una persona con cuerpo cuadrado, cabeza esférica, ropa, brazos y piernas."""
    glPushMatrix()
    draw_cuerpo()
    draw_cabeza()
    draw_brazo(-0.3)  # Brazo izquierdo
    draw_brazo(0.3)   # Brazo derecho
    draw_pierna(-0.15)  # Pierna izquierda
    draw_pierna(0.15)   # Pierna derecha
    glPopMatrix()

###########################################################################


# Variables globales para manejar la inercia
velocity_theta = 0.0  # Velocidad angular horizontal
velocity_phi = 0.0  # Velocidad angular vertical
friction = 0.95  # Factor de fricción para reducir la velocidad gradualmente

def handle_optical_flow():
    """
    Maneja los controles de la cámara basados en el flujo óptico y aplica inercia para simular 
    un movimiento suave y natural.
    """
    # Declaración de variables globales que se modificarán dentro de esta función.
    global theta, phi, velocity_theta, velocity_phi, p0, vgris

    # Captura un nuevo cuadro de la cámara.
    _, frame = cap.read()

    # Convierte el cuadro capturado a escala de grises, lo que facilita el cálculo del flujo óptico.
    fgris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Calcula el flujo óptico utilizando el método de Lucas-Kanade entre el cuadro actual y el anterior.
    # p0: puntos iniciales, p1: puntos calculados en el nuevo cuadro.
    # st: estado de los puntos (1 si se rastrean correctamente, 0 en caso contrario).
    # err: error de predicción para cada punto.
    p1, st, err = cv.calcOpticalFlowPyrLK(vgris, fgris, p0, None, **lkparm)

    # Si se han detectado puntos válidos (p1 no es None y hay puntos rastreados correctamente).
    if p1 is not None and st is not None:
        # Itera a través de los puntos rastreados (p1) y sus posiciones iniciales (p0).
        for i, (nv, vj) in enumerate(zip(p1, p0)):
            a, b = nv.ravel()  # Coordenadas del punto actual rastreado (nuevo).
            c, d = vj.ravel()  # Coordenadas del punto inicial (viejo).

            # Dibuja una línea desde la posición inicial (c, d) hasta la nueva posición (a, b).
            frame = cv.line(frame, (int(c), int(d)), (int(a), int(b)), (0, 255, 0), 1)

            # Dibuja un pequeño círculo en la posición nueva del punto.
            frame = cv.circle(frame, (int(a), int(b)), 2, (0, 0, 255), -1)

            # Ajustar la sensibilidad del movimiento detectado para calcular el control de la cámara.
            sensitivity = 0.01  # Factor para suavizar los movimientos detectados.

            # Si el punto se mueve hacia la izquierda (posición horizontal menor al centro menos 10).
            if a < width // 2 - 10:
                velocity_theta -= camera_speed * sensitivity * abs(a - (width // 2))  # Ajusta velocidad horizontal.
            # Si el punto se mueve hacia la derecha (posición horizontal mayor al centro más 10).
            elif a > width // 2 + 10:
                velocity_theta += camera_speed * sensitivity * abs(a - (width // 2))  # Ajusta velocidad horizontal.

            # Si el punto se mueve hacia arriba (posición vertical menor al centro menos 10).
            if b < height // 2 - 10:
                velocity_phi -= camera_speed * sensitivity * abs(b - (height // 2))  # Ajusta velocidad vertical.
            # Si el punto se mueve hacia abajo (posición vertical mayor al centro más 10).
            elif b > height // 2 + 10:
                velocity_phi += camera_speed * sensitivity * abs(b - (height // 2))  # Ajusta velocidad vertical.

    # Actualiza el cuadro previo (vgris) al actual (fgris) para la próxima iteración del flujo óptico.
    vgris = fgris.copy()

    # Devuelve el cuadro procesado con las visualizaciones (líneas y puntos) añadidas.
    return frame

def apply_inertia():
    """
    Aplica inercia a los ángulos de la cámara para simular un movimiento continuo y suave.
    """
    global theta, phi, velocity_theta, velocity_phi  # Variables globales para el control de la cámara.

    # Actualizar los ángulos de la cámara basándose en la velocidad actual.
    theta += velocity_theta  # Actualiza el ángulo horizontal (azimutal).
    phi = max(10, min(170, phi + velocity_phi))  # Actualiza el ángulo vertical (polar), limitado entre 10° y 170°.

    # Reducir gradualmente las velocidades aplicando fricción.
    velocity_theta *= friction  # Disminuye la velocidad horizontal usando un factor de fricción.
    velocity_phi *= friction  # Disminuye la velocidad vertical usando un factor de fricción.
    
def reset_camera():
    """
    Resetea la posición de la cámara y las velocidades a sus valores iniciales.
    """
    global theta, phi, radius, velocity_theta, velocity_phi  # Variables globales de la cámara.

    # Establecer los valores iniciales.
    theta = 0.0  # Ángulo horizontal de inicio.
    phi = 45.0  # Ángulo vertical inicial.
    radius = 70.0  # Distancia inicial de la cámara al punto objetivo.
    velocity_theta = 0.0  # Velocidad horizontal en 0.
    velocity_phi = 0.0  # Velocidad vertical en 0.


#Objeto carro pequeño
def draw_carroceria_inferior():
    """Dibuja la parte inferior de la carrocería del carro."""
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.2, 0.2)  # Gris

    # Frente
    glVertex3f(-2, 0, 1)
    glVertex3f(2, 0, 1)
    glVertex3f(2, 1, 1)
    glVertex3f(-2, 1, 1)

    # Atrás
    glVertex3f(-2, 0, -1)
    glVertex3f(2, 0, -1)
    glVertex3f(2, 1, -1)
    glVertex3f(-2, 1, -1)

    # Izquierda
    glVertex3f(-2, 0, -1)
    glVertex3f(-2, 0, 1)
    glVertex3f(-2, 1, 1)
    glVertex3f(-2, 1, -1)

    # Derecha
    glVertex3f(2, 0, -1)
    glVertex3f(2, 0, 1)
    glVertex3f(2, 1, 1)
    glVertex3f(2, 1, -1)

    # Arriba
    glVertex3f(-2, 1, -1)
    glVertex3f(2, 1, -1)
    glVertex3f(2, 1, 1)
    glVertex3f(-2, 1, 1)

    glEnd()

def draw_carroceria_superior():
    """Dibuja la parte superior de la carrocería con ventanas."""
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.2, 0.2)  # Gris

    # Frente
    glVertex3f(-1.5, 0, 0.8)
    glVertex3f(1.5, 0, 0.8)
    glVertex3f(1.5, 1, 0.8)
    glVertex3f(-1.5, 1, 0.8)

    # Atrás
    glVertex3f(-1.5, 0, -0.8)
    glVertex3f(1.5, 0, -0.8)
    glVertex3f(1.5, 1, -0.8)
    glVertex3f(-1.5, 1, -0.8)

    # Izquierda
    glVertex3f(-1.5, 0, -0.8)
    glVertex3f(-1.5, 0, 0.8)
    glVertex3f(-1.5, 1, 0.8)
    glVertex3f(-1.5, 1, -0.8)

    # Derecha
    glVertex3f(1.5, 0, -0.8)
    glVertex3f(1.5, 0, 0.8)
    glVertex3f(1.5, 1, 0.8)
    glVertex3f(1.5, 1, -0.8) #x,z,y

    glEnd()

    # Ventanas
    glColor3f(0.5, 0.8, 1)  # Azul claro para las ventanas
    glBegin(GL_QUADS)

    # Ventana frontal
    glVertex3f(-1.2, 0.2, 0.81)
    glVertex3f(1.2, 0.2, 0.81)
    glVertex3f(1.2, 0.8, 0.81)
    glVertex3f(-1.2, 0.8, 0.81)

    # Ventana trasera
    glVertex3f(-1.2, 0.2, -0.81)
    glVertex3f(1.2, 0.2, -0.81)
    glVertex3f(1.2, 0.8, -0.81)
    glVertex3f(-1.2, 0.8, -0.81)

    # Ventana lateral izquierda
    glVertex3f(-1.51, 0.2, -0.6)
    glVertex3f(-1.51, 0.2, 0.6)
    glVertex3f(-1.51, 0.8, 0.6)
    glVertex3f(-1.51, 0.8, -0.6)

    # Ventana lateral derecha
    glVertex3f(1.51, 0.2, -0.6)
    glVertex3f(1.51, 0.2, 0.6)
    glVertex3f(1.51, 0.8, 0.6)
    glVertex3f(1.51, 0.8, -0.6)

    glEnd()

def draw_llanta():
    """Dibuja una llanta tridimensional (cilíndrica)."""
    glColor3f(0, 0, 0)  # Negro para la llanta
    
    slices = 36  # Número de segmentos para aproximar el círculo
    radius = 0.5  # Radio de la llanta
    width = 0.2  # Grosor de la llanta

    # Dibuja la cara frontal del cilindro
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, width / 2)  # Centro del disco frontal
    for i in range(slices + 1):
        angle = 2 * pi * i / slices
        x = radius * cos(angle)
        y = radius * sin(angle)
        glVertex3f(x, y, width / 2)
    glEnd()

    # Dibuja la cara trasera del cilindro
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, -width / 2)  # Centro del disco trasero
    for i in range(slices + 1):
        angle = 2 * pi * i / slices
        x = radius * cos(angle)
        y = radius * sin(angle)
        glVertex3f(x, y, -width / 2)
    glEnd()

    # Conecta los bordes (paredes del cilindro)
    glBegin(GL_QUAD_STRIP)
    for i in range(slices + 1):
        angle = 2 * pi * i / slices
        x = radius * cos(angle)
        y = radius * sin(angle)
        glVertex3f(x, y, width / 2)   # Punto en el disco frontal
        glVertex3f(x, y, -width / 2)  # Punto en el disco trasero
    glEnd()
    
def draw_carro():
    """Dibuja el carro completo con movimiento."""
    glPushMatrix()
    # Aplicar transformación para mover el carro
    glTranslatef(carro_x, 0, carro_z)

    # Dibujar la carrocería inferior
    draw_carroceria_inferior()

    # Dibujar la carrocería superior
    glPushMatrix()
    glTranslatef(0, 1, 0)  # Ajuste para colocar la parte superior
    draw_carroceria_superior()
    glPopMatrix()

    # Dibujar las llantas
    # Lado izquierdo frontal
    glPushMatrix()
    glTranslatef(-1.7, 0.5, 1.0)
    draw_llanta()
    glPopMatrix()

    # Lado derecho frontal
    glPushMatrix()
    glTranslatef(1.7, 0.5, 1.0)
    draw_llanta()
    glPopMatrix()

    # Lado izquierdo trasero
    glPushMatrix()
    glTranslatef(-1.7, 0.5, -1.0)
    draw_llanta()
    glPopMatrix()

    # Lado derecho trasero
    glPushMatrix()
    glTranslatef(1.7, 0.5, -1.0)
    draw_llanta()
    glPopMatrix()

    glPopMatrix()  # Restaurar la matriz de transformación

    
def update_carro():
    """Actualiza la posición del carro."""
    global carro_x, carro_z, carro_direction_x, carro_direction_z

    # Movimiento en el eje X
    carro_x += 0.08 * carro_direction_x
    if carro_x > 10 or carro_x < -10:  # Cambiar dirección si llega al borde
        carro_direction_x *= -1

    # Movimiento en el eje Z
  #  carro_z += 0.03 * carro_direction_z
  #  if carro_z > 10 or carro_z < -10:  # Cambiar dirección si llega al borde
  #      carro_direction_z *= -1



###########################################################################

# Objeto camion
def draw_cuerpo_camion():
    """Dibuja el cuerpo de la carrocería de un autobús con ventanas, parabrisas y puerta."""
    glBegin(GL_QUADS)
    glColor3f(0.7, 0, 0)  # Azul para el cuerpo

    # Frente
    glVertex3f(-3, 0, 1)
    glVertex3f(3, 0, 1)
    glVertex3f(3, 3, 1)
    glVertex3f(-3, 3, 1)

    # Atrás
    glVertex3f(-3, 0, -1)
    glVertex3f(3, 0, -1)
    glVertex3f(3, 3, -1)
    glVertex3f(-3, 3, -1)

    # Izquierda
    glVertex3f(-3, 0, -1)
    glVertex3f(-3, 0, 1)
    glVertex3f(-3, 3, 1)
    glVertex3f(-3, 3, -1)

    # Derecha
    glVertex3f(3, 0, -1)
    glVertex3f(3, 0, 1)
    glVertex3f(3, 3, 1)
    glVertex3f(3, 3, -1)

    # Arriba
    glVertex3f(-3, 3, -1)
    glVertex3f(3, 3, -1)
    glVertex3f(3, 3, 1)
    glVertex3f(-3, 3, 1)

    glEnd()

    # Ventanas laterales
    glColor3f(0.5, 0.8, 1)  # Azul claro para las ventanas
    glBegin(GL_QUADS)

    for i in range(-3, 3):  # Ventanas de atrás
        inicio_x = -3.01
        inicio_y = 2
        inicio_z = 0.3 * i
        glVertex3f(inicio_x, inicio_y, inicio_z)
        glVertex3f(inicio_x, inicio_y, inicio_z + 0.2)
        glVertex3f(inicio_x, inicio_y + 0.8, inicio_z + 0.2)
        glVertex3f(inicio_x, inicio_y + 0.8, inicio_z)

    for i in range(-3, 3):  # Parabrisas
        inicio_x = 3.01
        inicio_y = 1.3
        inicio_z = 0.3 * i
        glVertex3f(inicio_x, inicio_y, inicio_z)
        glVertex3f(inicio_x, inicio_y, inicio_z + 0.3)
        glVertex3f(inicio_x, inicio_y + 0.8, inicio_z + 0.3)
        glVertex3f(inicio_x, inicio_y + 0.8, inicio_z)

    # Ventana lateral
    glVertex3f(-2.5, 1.5, -1.01)
    glVertex3f(2.5, 1.5, -1.01)
    glVertex3f(2.5, 2.8, -1.01)
    glVertex3f(-2.5, 2.8, -1.01)

    # Vantana lateral
    glVertex3f(-2.5, 1.5, 1.01)
    glVertex3f(1.5, 1.5, 1.01)
    glVertex3f(1.5, 2.8, 1.01)
    glVertex3f(-2.5, 2.8, 1.01)

    glEnd()

    # Puerta lateral derecha
    glColor3f(0.7, 0.7, 0.7)  # Gris claro para la puerta
    glBegin(GL_QUADS)

    
    # Definición de los 4 vértices de la puerta rectangular
    glVertex3f(1.8, 0.5, 1.01)   # Vértice inferior izquierdo
    glVertex3f(2.8, 0.5, 1.01)   # Vértice inferior derecho
    glVertex3f(2.8, 2.8, 1.01) # Vértice superior derecho
    glVertex3f(1.8, 2.8, 1.01) # Vértice superior izquierdo

    glEnd()




def draw_camion():
    """Dibuja el camión completo, ajustando las llantas al tamaño del cuerpo."""
    glPushMatrix()  # Guardar la matriz actual
    glTranslatef(camion_x, 0, camion_z)  # Aplicar la transformación de posición

    # Dibujar el cuerpo del camión
    draw_cuerpo_camion()

    # Dibujar las llantas
    # Lado izquierdo frontal
    glPushMatrix()
    glTranslatef(-1.8, 0, 1.1)  # Ajuste para el borde izquierdo y frontal
    draw_llanta()
    glPopMatrix()

    # Lado derecho frontal
    glPushMatrix()
    glTranslatef(1.8, 0, 1.1)  # Ajuste para el borde derecho y frontal
    draw_llanta()
    glPopMatrix()

    # Lado izquierdo trasero
    glPushMatrix()
    glTranslatef(-1.8, 0, -1.1)  # Ajuste para el borde izquierdo y trasero
    draw_llanta()
    glPopMatrix()

    # Lado derecho trasero
    glPushMatrix()
    glTranslatef(1.8, 0, -1.1)  # Ajuste para el borde derecho y trasero
    draw_llanta()
    glPopMatrix()

    glPopMatrix()  # Restaurar la matriz original




def update_camion():
    """Actualiza la posición del carro."""
    global camion_x, camion_z, camion_direction_x, camion_direction_z

    # Movimiento en el eje X
    camion_x += 0.03 * camion_direction_x
    if camion_x > 10 or camion_x < -10:  # Cambiar dirección si llega al borde
        camion_direction_x *= -1

    # Movimiento en el eje Z
   # camion_z += 0.03 * camion_direction_z
   # if camion_z > 10 or camion_z < -10:  # Cambiar dirección si llega al borde
   #     camion_direction_z *= -1


#####################################################################
#objeto: CASAS
def draw_cube():
    """Dibuja el cubo (base de la casa)"""
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.3, 0.5)  # Marrón para todas las caras

    # Frente
    glVertex3f(-1, 0, 1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 8, 1)
    glVertex3f(-1, 8, 1)

    # Atrás     X  Y   Z
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 8, -1)
    glVertex3f(-1, 8, -1)

    # Izquierda
    glVertex3f(-1, 0, -1)
    glVertex3f(-1, 0, 1)
    glVertex3f(-1, 8, 1)
    glVertex3f(-1, 8, -1)

    # Derecha
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 8, 1)
    glVertex3f(1, 8, -1)

    # Arriba
    glColor3f(0.2, 0.2, 0.2)  # Color diferente para el techo
    glVertex3f(-1, 8, -1)
    glVertex3f(1, 8, -1)
    glVertex3f(1, 8, 1)
    glVertex3f(-1, 8, 1)

    # Abajo
    glColor3f(0.6, 0.4, 0.2)  # Suelo más oscuro
    glVertex3f(-1,0 , -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(-1, 0, 1)
    glEnd()

def draw_roof():
    """Dibuja el techo (pirámide)"""
    glBegin(GL_TRIANGLES)
    glColor3f(0.4, 0.55, 0.5)  # Rojo brillante

    # Frente
    glVertex3f(-1, 8, 1)
    glVertex3f(1, 8, 1)
    glVertex3f(0, 11, 0)

    # Atrás     x  y   z 
    glVertex3f(-1, 8, -1)
    glVertex3f(1, 8, -1)
    glVertex3f(0, 11, 0)

    # Izquierda
    glVertex3f(-1, 8, -1)
    glVertex3f(-1, 8, 1)
    glVertex3f(0, 11, 0)

    # Derecha
    glVertex3f(1, 8, -1)
    glVertex3f(1, 8, 1)
    glVertex3f(0, 11, 0)
    glEnd()

def draw_house():
    """Dibuja una casa (base + techo)"""
    draw_cube()  # Base de la casa
    draw_roof()  # Techos   

#####################################################################
#objeto: EDIFICIOS 1
def draw_cube6():
    """Dibuja el cubo (base de la casa)"""
    glBegin(GL_QUADS)
    glColor3f(0.4, 0.3, 0.4)  # Marrón para todas las caras

    # Frente
    glVertex3f(-1, 0, 1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 8, 1)
    glVertex3f(-1, 8, 1)

    # Atrás     X  Y   Z
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 8, -1)
    glVertex3f(-1, 8, -1)

    # Izquierda
    glVertex3f(-1, 0, -1)
    glVertex3f(-1, 0, 1)
    glVertex3f(-1, 8, 1)
    glVertex3f(-1, 8, -1)

    # Derecha
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 8, 1)
    glVertex3f(1, 8, -1)

    # Arriba
    glColor3f(0.5, 0.5, 0.5)  # Color diferente para el techo
    glVertex3f(-1, 8, -1)
    glVertex3f(1, 8, -1)
    glVertex3f(1, 8, 1)
    glVertex3f(-1, 8, 1)

    # Abajo
    glColor3f(0.6, 0.4, 0.2)  # Suelo más oscuro
    glVertex3f(-1,0 , -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(-1, 0, 1)
    glEnd()



def draw_edificio1():
    """Dibuja una casa (base + techo)"""
    draw_cube6()  # Base de la casa
    



#####################################################################
#objeto: EDIFICIOS 2
def draw_cube7():
    """Dibuja el cubo (base de la casa)"""
    glBegin(GL_QUADS)
    glColor3f(0.6, 0.6, 0.3)  # Marrón para todas las caras

    # Frente
    glVertex3f(-1, 0, 1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 7, 1)
    glVertex3f(-1, 7, 1)

    # Atrás     X  Y   Z
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 7, -1)
    glVertex3f(-1, 7, -1)

    # Izquierda
    glVertex3f(-1, 0, -1)
    glVertex3f(-1, 0, 1)
    glVertex3f(-1, 7, 1)
    glVertex3f(-1, 7, -1)

    # Derecha
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 7, 1)
    glVertex3f(1, 7, -1)

    # Arriba
    glColor3f(0.4, 0.4, 0.4)  # Color diferente para el techo
    glVertex3f(-1, 7, -1)
    glVertex3f(1, 7, -1)
    glVertex3f(1, 7, 1)
    glVertex3f(-1, 7, 1)

    # Abajo
    glColor3f(0.6, 0.4, 0.2)  # Suelo más oscuro
    glVertex3f(-1,0 , -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(-1, 0, 1)
    glEnd()



def draw_edificio2():
    """Dibuja una casa (base + techo)"""
    draw_cube7()  # Base de la casa
    



#####################################################################
#objeto: EDIFICIOS 3
def draw_cube8():
    """Dibuja el cubo (base de la casa)"""
    glBegin(GL_QUADS)
    glColor3f(0.4, 0.7, 0.5)  # Marrón para todas las caras

    # Frente
    glVertex3f(-1, 0, 1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 6, 1)
    glVertex3f(-1, 6, 1)

    # Atrás     X  Y   Z
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 6, -1)
    glVertex3f(-1, 6, -1)

    # Izquierda
    glVertex3f(-1, 0, -1)
    glVertex3f(-1, 0, 1)
    glVertex3f(-1, 6, 1)
    glVertex3f(-1, 6, -1)

    # Derecha
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 6, 1)
    glVertex3f(1, 6, -1)

    # Arriba
    glColor3f(0.2, 0.2, 0.2)  # Color diferente para el techo
    glVertex3f(-1, 6, -1)
    glVertex3f(1, 6, -1)
    glVertex3f(1, 6, 1)
    glVertex3f(-1, 6, 1)

    # Abajo
    glColor3f(0.6, 0.4, 0.2)  # Suelo más oscuro
    glVertex3f(-1,0 , -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(-1, 0, 1)
    glEnd()

def draw_roof2():
    """Dibuja el techo (pirámide)"""
    glBegin(GL_TRIANGLES)
    glColor3f(0.6, 0.6, 0.5)  # Rojo brillante

    # Frente
    glVertex3f(-1, 6, 1)
    glVertex3f(1, 6, 1)
    glVertex3f(0, 8, 0)

    # Atrás     x  y   z 
    glVertex3f(-1, 6, -1)
    glVertex3f(1, 6, -1)
    glVertex3f(0, 8, 0)

    # Izquierda
    glVertex3f(-1, 6, -1)
    glVertex3f(-1, 6, 1)
    glVertex3f(0, 8, 0)

    # Derecha
    glVertex3f(1, 6, -1)
    glVertex3f(1, 6, 1)
    glVertex3f(0, 8, 0)
    glEnd()

def draw_edificio3():
    """Dibuja una casa (base + techo)"""
    draw_cube8()  # Base de la casa
    draw_roof2()  # Techos   

#####################################################################


#Objeto: CAJA DE REGALO
def draw_cube2(): 
    """Dibuja el cubo (arriba de la caja))"""
    glBegin(GL_QUADS)
    glColor3f(1, 0, 0)  # Marrón para todas las caras

    # Frente
    glVertex3f(-1, 0, 1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 5, 1)
    glVertex3f(-1, 5, 1)

    # Atrás     X  Y   Z
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 5, -1)
    glVertex3f(-1, 5, -1)

    # Izquierda
    glVertex3f(-1, 0, -1)
    glVertex3f(-1, 0, 1)
    glVertex3f(-1, 5, 1)
    glVertex3f(-1, 5, -1)

    # Derecha
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 5, 1)
    glVertex3f(1, 5, -1)

    # Arriba
    glColor3f(1, 0, 0)  # Color diferente para el techo
    glVertex3f(-1, 5, -1)
    glVertex3f(1, 5, -1)
    glVertex3f(1, 5, 1)
    glVertex3f(-1, 5, 1)

    # Abajo
    glColor3f(0.6, 0.4, 0.2)  # Suelo más oscuro
    glVertex3f(-1,0 , -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(-1, 0, 1)
    glEnd()



def draw_cube3():
    """Dibuja el cubo (arriba de la tapa)"""
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)  # Marrón para todas las caras

    # Frente
    glVertex3f(-1, 0, 1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 5, 1)
    glVertex3f(-1, 5, 1)

    # Atrás     X  Y   Z
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 5, -1)
    glVertex3f(-1, 5, -1)

    # Izquierda
    glVertex3f(-1, 0, -1)
    glVertex3f(-1, 0, 1)
    glVertex3f(-1, 5, 1)
    glVertex3f(-1, 5, -1)

    # Derecha
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 5, 1)
    glVertex3f(1, 5, -1)

    # Arriba
    glColor3f(1,1 ,1)  # Color diferente para el techo
    glVertex3f(-1, 5, -1)
    glVertex3f(1, 5, -1)
    glVertex3f(1, 5, 1)
    glVertex3f(-1, 5, 1)

    # Abajo
    glColor3f(0.6, 0.4, 0.2)  # Suelo más oscuro
    glVertex3f(-1,0 , -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(-1, 0, 1)
    glEnd()


def draw_cube4():
    """Dibuja el cubo (base de la casa)"""
    glBegin(GL_QUADS)
    glColor3f(0, 0, 1)  # Marrón para todas las caras

    # Frente
    glVertex3f(-1, 0, 1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 5, 1)
    glVertex3f(-1, 5, 1)

    # Atrás     X  Y   Z
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 5, -1)
    glVertex3f(-1, 5, -1)

    # Izquierda
    glVertex3f(-1, 0, -1)
    glVertex3f(-1, 0, 1)
    glVertex3f(-1, 5, 1)
    glVertex3f(-1, 5, -1)

    # Derecha
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 5, 1)
    glVertex3f(1, 5, -1)

    # Arriba
    glColor3f(0, 0, 1)  # Color diferente para el techo
    glVertex3f(-1, 5, -1)
    glVertex3f(1, 5, -1)
    glVertex3f(1, 5, 1)
    glVertex3f(-1, 5, 1)

    # Abajo
    glColor3f(0.6, 0.4, 0.2)  # Suelo más oscuro
    glVertex3f(-1,0 , -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(-1, 0, 1)
    glEnd()




###############################################################################
#objeto: SANTA CLAUS

def draw_trineos():
    """Dibuja el tronco del árbol como un cilindro"""
    glPushMatrix()
    glColor3f(0.6, 0.3, 0.1)  # Marrón para el tronco
    glRotatef(-90, 1, 0, 0)  # Rota para orientar el cilindro verticalmente
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.3, 0.3, 2.0, 32, 32)  # Radio y altura del cilindro
    glPopMatrix()


##############################################################################
#Objeto: PINO DE NAVIDAD

def draw_trunk2():
    """Dibuja el tronco del árbol como un cilindro"""
    glPushMatrix()
    glColor3f(0.6, 0.3, 0.1)  # Marrón para el tronco
    glRotatef(-90, 1, 0, 0)  # Rota para orientar el cilindro verticalmente
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.3, 0.3, 2.0, 32, 32)  # Radio y altura del cilindro
    glPopMatrix()

def draw_foliage2():
    """Dibuja el techo (pirámide)"""
    glBegin(GL_TRIANGLES)
    glColor3f(0, 1, 0)  # Rojo brillante
    

    # Frente
    glVertex3f(-1, 2, 1)
    glVertex3f(1, 2, 1)
    glVertex3f(0, 7, 0)

    # Atrás     x  y   z 
    glVertex3f(-1, 2, -1)
    glVertex3f(1, 2, -1)
    glVertex3f(0, 7, 0)

    # Izquierda
    glVertex3f(-1, 2, -1)
    glVertex3f(-1, 2, 1)
    glVertex3f(0, 7, 0)

    # Derecha
    glVertex3f(1, 2, -1)
    glVertex3f(1, 2, 1)
    glVertex3f(0, 7, 0)
    glEnd()




def draw_tree2():
    """Dibuja un árbol completo"""
    draw_trunk2()
    draw_foliage2()

def draw_pino():
    # Dibujar el árbol sobre el regalo
    glPushMatrix()
    glTranslatef(1.8, 0.1, -6)  # Posicionar el pino encima de la caja
    glScalef(1.5, 1.5, 1.5)  # Escalar el pino para que no sea demasiado grande
    draw_tree2()
    glPopMatrix()

################################################################################'
#Objeto: CAJA DE REGALO

def draw_gift():
    """Dibuja un regalo con tapa, cintas y moño decorativo en la parte superior correctamente orientado."""
    # Dibujar la caja
    glPushMatrix()
    glColor3f(1, 0.0, 0.0)  # Rojo para la caja
    glScalef(0.5, 0.25, 0.5)  # Más ancha y baja
    draw_cube2()  # Usar la función existente para la base de la caja
    glPopMatrix()

    # Dibujar la tapa del regalo
    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)  # Blanco para la tapa
    glTranslatef(0.0, 1.25, 0.0)  # Posicionar la tapa justo encima de la caja
    glScalef(0.55, 0.05, 0.55)  # Un poco más grande y delgada
    draw_cube3()
    glPopMatrix()

    # Dibujar las cintas cruzadas
    glPushMatrix()
    glColor3f(0.0, 0.0, 1.0)  # Azul para las cintas
    glTranslatef(0.0, 1.5, 0.0)  # Encima de la tapa
    glScalef(0.55, 0.01, 0.1)  # Cinta horizontal
    draw_cube2()
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.0, 0.0, 1.0)  # Azul para las cintas
    glTranslatef(0.0, 1.5, 0.0)  # Encima de la tapa
    glScalef(0.1, 0.01, 0.55)  # Cinta vertical
    draw_cube2()
    glPopMatrix()

    # Dibujar el moño decorativo
    for angle in range(0, 360, 45):  # Crear pétalos del moño en forma circular
        glPushMatrix()
        glColor3f(0.0, 0.0, 1.0)  # Azul para el moño
        glTranslatef(0.0, 1.45, 0.0)  # Encima de la tapa, más arriba
        glRotatef(angle, 0, 1, 0)  # Rotar cada pétalo
        glTranslatef(0.2, 0.0, 0.0)  # Mover el pétalo hacia afuera
        glScalef(0.05, 0.025, 0.2)  # Dar forma de pétalo
        draw_cube4()
        glPopMatrix()

    # Centro del moño
    glPushMatrix()
    glColor3f(0.0, 0.0, 1.0)  # Azul para el centro del moño
    glTranslatef(0.0, 1.6, 0.0)  # Aún más arriba para el centro
    quadric = gluNewQuadric()
    gluSphere(quadric, 0.1, 32, 32)  # Esfera pequeña
    glPopMatrix()



############################################################################
#Objeto: Muneco de nieve

def draw_snowman():
    """Dibuja un muñeco de nieve"""
    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)  # Blanco para el muñeco
    quadric = gluNewQuadric()
    gluSphere(quadric, 0.6, 32, 32)  # Bola inferior
    glTranslatef(0.0, 1, 0)  # Bola media
    gluSphere(quadric, 0.4, 32, 32)
    glTranslatef(0.0, 0.6, 0.0)  # Cabeza
    gluSphere(quadric, 0.3, 32, 32)
    glPopMatrix()

###########################################################################
#Objeto: PARQUE

def draw_trunk():
    """Dibuja el tronco del árbol como un cilindro"""
    glPushMatrix()
    glColor3f(0.6, 0.3, 0.1)  # Marrón para el tronco
    glRotatef(-90, 1, 0, 0)  # Rota para orientar el cilindro verticalmente
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.3, 0.3, 2.0, 32, 32)  # Radio y altura del cilindro
    glPopMatrix()

def draw_foliage():
    """Dibuja las hojas del árbol como una esfera"""
    glPushMatrix()
    glColor3f(0.1, 0.8, 0.1)  # Verde para las hojas
    glTranslatef(0.0, 2, 0.0)  # Posicionar las hojas encima del tronco
    quadric = gluNewQuadric()
    gluSphere(quadric, 1.0, 32, 32)  # Radio de la esfera
    glPopMatrix()

def draw_tree():
    """Dibuja un árbol completo"""
    draw_trunk()
    draw_foliage()



def draw_park():
    """Dibuja un parque con un árbol y un lago"""
    # Césped
    glPushMatrix()
    glBegin(GL_QUADS)
    glColor3f(0.6, 0.7, 0.2)  # Verde para el césped
    glVertex3f(-6, 0.1, -6)
    glVertex3f(6, 0.1, -6)
    glVertex3f(6, 0.1, 6)
    glVertex3f(-6, 0.1, 6)
    glEnd()
    glPopMatrix()

    # Lago
    glPushMatrix()
    glColor3f(0.2, 0.4, 0.8)  # Azul para el lago
    glTranslatef(1, 0.1, -1)  # Posicionar el lago
    glRotatef(-90, 1, 0, 0)   # Girar para que el cilindro quede horizontal
    quadric = gluNewQuadric()
    gluCylinder(quadric, 1.4, 0, 0.1, 32, 32)  # Cilindro con altura baja para simular un lago
    glPopMatrix()

    # Árbol
    glPushMatrix()
    glTranslatef(-1, 0, 1)  # Posicionar el árbol en el parque
    draw_tree()
    glPopMatrix()


############################################################################
#Objeto: SANTA CLAUS

    # Dibujar a Santa Claus
    draw_santa()
    draw_trineos()
    draw_trineos2()
    draw_trineos3()
    draw_trineos4()

def draw_santa():
    """Dibuja a Santa Claus"""
    glPushMatrix()
    glColor3f(0.6, 0.0, 0.0)  # Rojo para el traje
    glTranslatef(santa_x, 11, santa_z)  # Posición dinámica de Santa Claus
    quadric = gluNewQuadric()
    gluSphere(quadric, 0.5, 32, 32)  # Cabeza
    glTranslatef(0.0, -0.8, 0.0)  # Mover para el cuerpo
    gluCylinder(quadric, 0.5, 0.3, 1.0, 32, 32)  # Cuerpo
    glPopMatrix()

def draw_trineos():
    """dibuja trineos de santa"""
    glPushMatrix()
    glColor3f(0.8, 0.6, 0.1)  # marron para trineos
    glTranslatef(santa_x+1, 11, santa_z)  # Posición dinámica de Santa Claus
    quadric = gluNewQuadric()
    
    glTranslatef(0.0, -0.8, 0.0)  # Mover para el cuerpo
    gluCylinder(quadric, 0.5, 0.3, 1.0, 32, 32)  # Cuerpo
    glPopMatrix()

def draw_trineos2():
    """dibuja trineos de santa"""
    glPushMatrix()
    glColor3f(0.8, 0.6, 0.1)  # marron para trineos
    glTranslatef(santa_x+2, 11, santa_z)  # Posición dinámica de Santa Claus
    quadric = gluNewQuadric()
    
    glTranslatef(0.0, -0.8, 0.0)  # Mover para el cuerpo
    gluCylinder(quadric, 0.5, 0.3, 1.0, 32, 32)  # Cuerpo
    glPopMatrix()

def draw_trineos3():
    """dibuja trineos de santa"""
    glPushMatrix()
    glColor3f(0.8, 0.6, 0.1)  # marron para trineos
    glTranslatef(santa_x+3, 11, santa_z)  # Posición dinámica de Santa Claus
    quadric = gluNewQuadric()
    
    glTranslatef(0.0, -0.8, 0.0)  # Mover para el cuerpo
    gluCylinder(quadric, 0.5, 0.3, 1.0, 32, 32)  # Cuerpo
    glPopMatrix()

def draw_trineos4():
    """dibuja trineos de santa"""
    glPushMatrix()
    glColor3f(0.8, 0.6, 0.1)  # marron para trineos
    glTranslatef(santa_x+4, 11, santa_z)  # Posición dinámica de Santa Claus
    quadric = gluNewQuadric()
    
    glTranslatef(0.0, -0.8, 0.0)  # Mover para el cuerpo
    gluCylinder(quadric, 0.5, 0.3, 1.0, 32, 32)  # Cuerpo
    glPopMatrix()


def update_santa():
    """Actualiza la posición de Santa Claus"""
    global santa_x, santa_z, santa_direction_x, santa_direction_z

    # Movimiento en el eje X
    santa_x += 0.02 * santa_direction_x
    if santa_x > 10 or santa_x < -10:  # Cambiar dirección si llega al borde
        santa_direction_x *= -1

    








def key_callback(window):
    """Procesa las entradas de teclado para mover la cámara"""
    global theta, phi, radius, velocity_theta, velocity_phi  # Variables de control de la cámara.

    # Detectar teclas presionadas.
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:  # Tecla W presionada (mover hacia arriba).
        phi = max(10, min(170, phi - camera_speed))  # Ajusta phi hacia arriba con límites.
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:  # Tecla S presionada (mover hacia abajo).
        phi = max(30, min(170, phi + camera_speed))  # Ajusta phi hacia abajo con un límite mínimo de 30°.
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:  # Tecla A presionada (mover hacia la izquierda).
        theta -= camera_speed  # Reduce el ángulo horizontal.
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:  # Tecla D presionada (mover hacia la derecha).
        theta += camera_speed  # Incrementa el ángulo horizontal.
    if glfw.get_key(window, glfw.KEY_R) == glfw.PRESS:  # Tecla R presionada (resetear posición).
        reset_camera()  # Llama a la función para resetear la cámara.

def draw_scene():
    """Dibuja toda la escena, incluyendo el suelo, las calles, las piedras y las montañas"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    camera_pos = spherical_to_cartesian(radius, theta, phi)
    gluLookAt(*camera_pos, *camera_target, 0, 1, 0)  # Vector hacia arriba

    # Dibujar el suelo
    draw_ground()

    # Dibujar las calles
    draw_street()

    update_snowflakes()  # Actualizar las posiciones de los copos de nieve
    draw_snowflakes()    # Dibujar los copos de nieve
    
    

 # Dibujar el carro
    draw_carro()

    

        # Dibujar el carro  en diferentes posiciones
    positions = [
        (-3, 0.5, 15),  # carro 1
#        (-5, 0.5, -9),   # carro 2
    ]
    
    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)  # Mover carro a la posición actual
        draw_carro()        # Dibujar carro #linea 709
        glPopMatrix()





   # draw_camion()
        
    # Dibujar el camion  en diferentes posiciones
    positions = [
        (10, 0.5, 14),  # camion 1
        (-10, 0.5, -4),   # camion 2
    ]
    
    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)  # Mover camion a la posición actual
        draw_camion()        # Dibujar camion
        glPopMatrix()






    # Dibujar las personas en diferentes posiciones
    positions = [
        (2, 0.5, 5),  # Perons 1
        (-2, 0.5, 5),   # Persona 2
    ]
    
    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)  # Mover carro a la posición actual
        draw_persona()        # Dibujar persona
        glPopMatrix()

    # Dibujar las piedras
    for stone in stones:
        x, y, z, size = stone
        draw_stone(x, y, z, size)

    # Dibujar las montañas en las esquinas inferiores
    draw_mountain(15, -15)  # Montaña en la esquina inferior derecha
    draw_mountain(-15, -15)  # Montaña en la esquina inferior izquierda





 # Dibujar las cajas regalo en diferentes posiciones
    positions = [
        (2.5, 0, -11),  # refalo 1
        (-2.5, 0, -11),   # regalo 2
        (0, 0, -16),   # regalo 3
        (0, 0, -13),
        (-2.5, 0, -16), 
        (2.5, 0, -16), 
    ]
    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)  # Mover reghalo a la posición actual
        draw_gift()        # Dibujar regalo
        glPopMatrix()

    

#posicion de los munecos de nieve
    positions = [
        (-4.5, 1, -11),  # muneco 1
        (4.5, 1 , -11),   # muneco 2
        
    ]
    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)  # Mover muneco a la posición actual
        draw_snowman()        # Dibujar muneco
        glPopMatrix()



    # Dibujar un regalo con pino en la escena principal
    glPushMatrix()
    glTranslatef(-2, 0, -5)  # Ajusta las coordenadas para posicionar el regalo con el pino
    draw_pino()
    glPopMatrix()

    


    # Dibujar las casas en diferentes posiciones
    positions = [
        (-11, 0, -11),  # Casa 1
        (11, 0, -11),   # Casa 2
        (-11, 0, 11),   # Casa 3
        (11, 0, 11),
        (-11, 0, -5),
        (11, 0, -5),
        (-11, 0, 5), 
        (11, 0, 5),
        
    ]
    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)  # Mover la casa a la posición actual
        draw_house()        # Dibujar la casa
        glPopMatrix()



    # Dibujar edificios en diferentes posiciones
    positions = [
        (-5, 0, -18),  # edificio 1
        (5, 0, -18),   # edificio 2
        (-5, 0, 11),   # edificio 3
        (5, 0, 11),
    ]
    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)  # Mover la casa a la posición actual
        draw_edificio1()        # Dibujar la casa
        glPopMatrix()




# Dibujar edificios2 en diferentes posiciones
    positions = [
        (-3, 0, -18),  # edificio 1
        (3, 0, -18),   # edificio 2
        (-3, 0, 11),   # edificio 3
        (3, 0, 11),
        (-11, 0, -3),
        (11, 0, -3),
        (-11, 0, 3), 
        (11, 0, 3),
    ]
    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)  # Mover la casa a la posición actual
        draw_edificio2()        # Dibujar la casa
        glPopMatrix()



# Dibujar edificios3 en diferentes posiciones
    positions = [
        
        (0, 0, -18),   # edificio 2 es el de atras

        (0, 0, 11),   # edificio 3 el de enfrente
        (5, 0, 14),
        (-5, 0, 14),

        (-11, 0, 0),    # el de la izquierda
        (-14, 0, -5), 
        (-14, 0, 5), 

        (11, 0, 0),     #derecha
        (14, 0, -5),
        (14, 0, 5),
        



    ]
    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)  # Mover la casa a la posición actual
        draw_edificio3()        # Dibujar la casa
        glPopMatrix()




    # Dibujar el parque en el centro
    glPushMatrix()
    glTranslatef(0, 0, 0)  # Posicionar el parque en el centro
    draw_park()
    glPopMatrix()





    glfw.swap_buffers(window)

def main():
    global theta, phi, radius, vgris, window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Ciudad con calles y piedras", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    key_callback(window)  # Registrar el callback de teclado
    glViewport(0, 0, width, height)
    init()

    # Generar las piedras estáticas con posiciones fijas y color café
    for _ in range(800):  # Crear numero de piedras
        # Generar posición aleatoria para la piedra
        x = random.uniform(-20, 20)
        z = random.uniform(-20, 20)

        y = 0.1  # Altura en el eje Y (encima del suelo)
        size = random.uniform(0.2, 0.5)  # Tamaño aleatorio de las piedras
        stones.append((x, y, z, size))  # Almacenar la posición y tamaño de la piedra
        
    # Inicializar OpenCV.
    _, vframe = cap.read()  # Captura un cuadro inicial desde la cámara.
    vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)

    # Bucle principal
    while not glfw.window_should_close(window):
        frame = handle_optical_flow()
        apply_inertia()  # Aplica inercia a la cámara para movimiento suave.
        
        update_camion()
        update_santa()
        update_carro()
        
        draw_scene()
        glfw.poll_events()
        
        # Muestra el cuadro capturado de la cámara con visualización del flujo óptico.
        cv.imshow("malla", frame)
        if cv.waitKey(1) & 0xFF == 27:  # Termina si se presiona la tecla Esc.
            break

    # Finalización y liberación de recursos.
    cap.release()  # Libera la cámara.
    cv.destroyAllWindows()  # Cierra todas las ventanas de OpenCV.
    glfw.terminate()

if __name__ == "__main__":
    main()
```