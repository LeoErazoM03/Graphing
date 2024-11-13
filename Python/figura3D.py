import glfw
from OpenGL.GL import glClear, glClearColor, glBegin, glEnd, glVertex2f, glColor3f, GL_COLOR_BUFFER_BIT, GL_QUADS, glOrtho

def draw_square():
    glBegin(GL_QUADS)
    glColor3f(1.0, 0.0, 0.0)  # Color rojo
    glVertex2f(-0.5,  0.5)  # Vértice superior izquierdo
    glVertex2f( 0.5,  0.5)  # Vértice superior derecho
    glVertex2f( 0.5, -0.5)  # Vértice inferior derecho
    glVertex2f(-0.5, -0.5)  # Vértice inferior izquierdo
    glEnd()

def main():
    # Inicializar GLFW
    if not glfw.init():
        return

    # Crear la ventana con un contexto de OpenGL
    window = glfw.create_window(500, 500, "Cuadrado con GLFW", None, None)
    if not window:
        glfw.terminate()
        return

    # Hacer que el contexto de OpenGL sea actual para la ventana
    glfw.make_context_current(window)

    # Configurar la proyección ortográfica
    glOrtho(-1, 1, -1, 1, -1, 1)  # Configuración para un sistema de coordenadas 2D

    # Bucle principal
    while not glfw.window_should_close(window):
        # Limpiar el buffer de color
        glClear(GL_COLOR_BUFFER_BIT)

        # Dibujar el cuadrado
        draw_square()

        # Intercambiar buffers y procesar eventos
        glfw.swap_buffers(window)
        glfw.poll_events()

    # Terminar GLFW
    glfw.terminate()

if __name__ == "__main__":
    main()
