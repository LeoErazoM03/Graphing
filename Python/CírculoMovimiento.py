import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluNewQuadric, gluSphere, gluPerspective
import sys

# Variables globales para el ángulo de rotación y posición de la esfera
window = None
rotation_angle = 0.0  # Ángulo de rotación de la esfera
movement_offset = 0.0  # Offset para el movimiento horizontal
vertical_offset = 0.0  # Offset para el movimiento vertical
depth_offset = -5.0    # Posición inicial en el eje Z
depth_speed = -0.01    # Velocidad de alejamiento en el eje Z
movement_speed = 0.0009  # Velocidad del movimiento horizontal
vertical_speed = 0.0009  # Velocidad del movimiento vertical
movement_direction = .4  # Dirección del movimiento horizontal (1 derecha, -1 izquierda)
vertical_direction = .6  # Dirección del movimiento vertical (1 arriba, -1 abajo)

# Límites visibles del canvas (ajustados para la perspectiva)
canvas_limit = 2.0  # Límite horizontal inicial visible
canvas_vertical_limit = 2.0  # Límite vertical inicial visible
sphere_radius = 0.5  # Radio de la esfera

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Fondo negro
    glEnable(GL_DEPTH_TEST)            # Activar prueba de profundidad
    glEnable(GL_LIGHTING)              # Activar iluminación
    glEnable(GL_LIGHT0)                # Activar la luz 0

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 1.0, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    # Configuración de la luz
    light_pos = [1.0, 1.0, 1.0, 0.0]  # Posición de la luz
    light_color = [1.0, 1.0, 1.0, 1.0]  # Color de la luz blanca
    ambient_light = [0.2, 0.2, 0.2, 1.0]  # Luz ambiental

    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)

    # Configuración de las propiedades de material
    material_diffuse = [0.2, 0.6, 1.0, 1.0]  # Color difuso (azul claro)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)

def draw_sphere(radius=1, slices=32, stacks=32):
    global rotation_angle, movement_offset, vertical_offset, depth_offset
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(movement_offset, vertical_offset, depth_offset)  # Mover la esfera en todas las direcciones
    glRotatef(rotation_angle, 0, 1, 0)  # Rotar la esfera sobre su eje Y

    quadric = gluNewQuadric()
    gluSphere(quadric, radius, slices, stacks)  # Dibujar la esfera

    glfw.swap_buffers(window)

def update_motion():
    global rotation_angle, movement_offset, vertical_offset, depth_offset, depth_speed
    global movement_direction, vertical_direction, canvas_limit, canvas_vertical_limit

    # Actualizar el ángulo de rotación
    rotation_angle += 1
    if rotation_angle >= 360:
        rotation_angle = 0  # Reiniciar el ángulo después de una vuelta completa

    # Recalcular los límites visibles en función de la distancia (perspectiva)
    visible_scale = abs(depth_offset / 5.0)  # Escalar los límites en base a la distancia
    dynamic_canvas_limit = canvas_limit * visible_scale
    dynamic_canvas_vertical_limit = canvas_vertical_limit * visible_scale

    # Actualizar el movimiento horizontal
    movement_offset += movement_speed * movement_direction
    if movement_offset > (dynamic_canvas_limit - sphere_radius):  # Límite derecho
        movement_direction = -1  # Cambiar dirección hacia la izquierda
    elif movement_offset < -(dynamic_canvas_limit - sphere_radius):  # Límite izquierdo
        movement_direction = 1  # Cambiar dirección hacia la derecha

    # Actualizar el movimiento vertical
    vertical_offset += vertical_speed * vertical_direction
    if vertical_offset > (dynamic_canvas_vertical_limit - sphere_radius):  # Límite superior
        vertical_direction = -1  # Cambiar dirección hacia abajo
    elif vertical_offset < -(dynamic_canvas_vertical_limit - sphere_radius):  # Límite inferior
        vertical_direction = 1  # Cambiar dirección hacia arriba

    # Actualizar el alejamiento (movimiento en el eje Z)
    depth_offset += depth_speed
    if depth_offset < -50:  # Limitar el alejamiento si se desea
        depth_speed = 0  # Detener el alejamiento

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 500, 500
    window = glfw.create_window(width, height, "Esfera en Movimiento y Alejamiento", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_sphere(radius=sphere_radius)
        update_motion()  # Actualizar el movimiento y rotación
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
