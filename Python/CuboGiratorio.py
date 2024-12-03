import glfw
from OpenGL.GL import glClearColor, glEnable, glClear, glLoadIdentity, glTranslatef, glRotatef, glMatrixMode
from OpenGL.GL import glBegin, glColor3f, glVertex3f, glEnd, glFlush, glViewport
from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_TRIANGLES, GL_PROJECTION, GL_MODELVIEW
from OpenGL.GLU import gluPerspective
import sys

# Variables globales
window = None
angle_x, angle_y = 0, 0  # Ángulos de rotación en los ejes X e Y
velocidad_x, velocidad_y = 0.05, 0.05  # Velocidad de rotación

def init():
    # Configuración inicial de OpenGL
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Color de fondo
    glEnable(GL_DEPTH_TEST)  # Activar prueba de profundidad para 3D

    # Configuración de proyección
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 0.1, 50.0)

    # Cambiar a la matriz de modelo para los objetos
    glMatrixMode(GL_MODELVIEW)

def draw_octahedron():
    global angle_x, angle_y
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpiar pantalla y buffer de profundidad

    # Configuración de la vista del octaedro
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5)  # Alejar el octaedro para que sea visible
    glRotatef(angle_x, 1, 0, 0)   # Rotar el octaedro en el eje X
    glRotatef(angle_y, 0, 1, 0)   # Rotar el octaedro en el eje Y

    glBegin(GL_TRIANGLES)  # Iniciar el octaedro como un conjunto de caras triangulares

    # Vértices del octaedro
    vertices = [
        (0, 1, 0),   # Vértice superior
        (-1, 0, -1), # Vértice inferior izquierda trasera
        (1, 0, -1),  # Vértice inferior derecha trasera
        (1, 0, 1),   # Vértice inferior derecha delantera
        (-1, 0, 1),  # Vértice inferior izquierda delantera
        (0, -1, 0)   # Vértice inferior
    ]

    # Colores para cada cara
    colors = [
        (1.0, 0.0, 0.0),  # Rojo
        (0.0, 1.0, 0.0),  # Verde
        (0.0, 0.0, 1.0),  # Azul
        (1.0, 1.0, 0.0),  # Amarillo
        (1.0, 0.0, 1.0),  # Magenta
        (0.0, 1.0, 1.0),  # Cyan
        (0.5, 0.5, 0.5),  # Gris
        (1.0, 0.5, 0.0)   # Naranja
    ]

    # Caras del octaedro (en índices de vértices)
    faces = [
        (0, 1, 2),
        (0, 2, 3),
        (0, 3, 4),
        (0, 4, 1),
        (5, 2, 1),
        (5, 3, 2),
        (5, 4, 3),
        (5, 1, 4)
    ]

    # Dibujar las caras del octaedro
    for i, face in enumerate(faces):
        glColor3f(*colors[i % len(colors)])
        for vertex in face:
            glVertex3f(*vertices[vertex])

    glEnd()
    glFlush()

    glfw.swap_buffers(window)  # Intercambiar buffers para animación suave

def main():
    global window, angle_x, angle_y, velocidad_x, velocidad_y

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()

    # Crear ventana de GLFW
    width, height = 500, 500
    window = glfw.create_window(width, height, "Octaedro 3D Rotación Automática", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    # Configurar el contexto de OpenGL en la ventana
    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Bucle principal
    while not glfw.window_should_close(window):
        angle_x += velocidad_x  # Incrementar ángulo de rotación en X según la velocidad
        angle_y += velocidad_y  # Incrementar ángulo de rotación en Y según la velocidad
        draw_octahedron()
        glfw.poll_events()

    glfw.terminate()  # Cerrar GLFW al salir

if __name__ == "__main__":
    main()
