import glfw
from OpenGL.GL import glClearColor, glEnable, glClear, glLoadIdentity, glTranslatef, glRotatef, glMatrixMode
from OpenGL.GL import glBegin, glColor3f, glVertex3f, glEnd, glFlush, glViewport
from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_QUADS, GL_PROJECTION, GL_MODELVIEW
from OpenGL.GLU import gluPerspective
import sys

# Variables globales
window = None
angle_x, angle_y = 0, 0  # Ángulos de rotación en los ejes X e Y
last_x, last_y = None, None  # Última posición del ratón para calcular la diferencia

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

def draw_cube():
    global angle_x, angle_y
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpiar pantalla y buffer de profundidad

    # Configuración de la vista del cubo
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5)  # Alejar el cubo para que sea visible
    glRotatef(angle_x, 1, 0, 0)   # Rotar el cubo en el eje X
    glRotatef(angle_y, 0, 1, 0)   # Rotar el cubo en el eje Y

    glBegin(GL_QUADS)  # Iniciar el cubo como un conjunto de caras (quads)

    # Cada conjunto de cuatro vértices representa una cara del cubo
    glColor3f(1.0, 0.0, 0.0)  # Rojo
    glVertex3f( 1, 1,-1)
    glVertex3f(-1, 1,-1)
    glVertex3f(-1, 1, 1)
    glVertex3f( 1, 1, 1)

    glColor3f(0.0, 1.0, 0.0)  # Verde
    glVertex3f( 1,-1, 1)
    glVertex3f(-1,-1, 1)
    glVertex3f(-1,-1,-1)
    glVertex3f( 1,-1,-1)

    glColor3f(0.0, 0.0, 1.0)  # Azul
    glVertex3f( 1, 1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1,-1, 1)
    glVertex3f( 1,-1, 1)

    glColor3f(1.0, 1.0, 0.0)  # Amarillo
    glVertex3f( 1,-1,-1)
    glVertex3f(-1,-1,-1)
    glVertex3f(-1, 1,-1)
    glVertex3f( 1, 1,-1)

    glColor3f(1.0, 0.0, 1.0)  # Magenta
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1,-1)
    glVertex3f(-1,-1,-1)
    glVertex3f(-1,-1, 1)

    glColor3f(0.0, 1.0, 1.0)  # Cyan
    glVertex3f( 1, 1,-1)
    glVertex3f( 1, 1, 1)
    glVertex3f( 1,-1, 1)
    glVertex3f( 1,-1,-1)

    glEnd()
    glFlush()

    glfw.swap_buffers(window)  # Intercambiar buffers para animación suave

def mouse_callback(window, xpos, ypos):
    global angle_x, angle_y, last_x, last_y

    # Si es la primera vez que movemos el ratón, inicializamos last_x y last_y
    if last_x is None or last_y is None:
        last_x, last_y = xpos, ypos

    # Calcular las diferencias en el movimiento del ratón
    dx = xpos - last_x
    dy = ypos - last_y

    # Ajustar los ángulos de rotación en función del movimiento del ratón
    angle_x += dy * 0.1  # El factor 0.1 ajusta la sensibilidad
    angle_y += dx * 0.1

    # Actualizar las posiciones anteriores del ratón
    last_x, last_y = xpos, ypos

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()

    # Crear ventana de GLFW
    width, height = 500, 500
    window = glfw.create_window(width, height, "Cubo 3D Controlado por Ratón", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    # Configurar el contexto de OpenGL en la ventana
    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Configurar el callback de ratón
    glfw.set_cursor_pos_callback(window, mouse_callback)

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_cube()
        glfw.poll_events()

    glfw.terminate()  # Cerrar GLFW al salir

if __name__ == "__main__":
    main()