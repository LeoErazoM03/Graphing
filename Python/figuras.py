from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image

def load_texture(image_path):
    # Generar y enlazar una textura
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    # Cargar imagen desde el archivo
    img = Image.open(image_path)
    img = img.convert("RGB")  # Convertir a RGB explícitamente
    img_data = img.tobytes("raw", "RGB", 0, -1)
    
    # Configurar la textura
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0,
                 GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    return texture_id

def init_lighting():
    # Configuración de iluminación
    glEnable(GL_LIGHTING)  # Habilitar iluminación
    glEnable(GL_LIGHT0)  # Activar la luz 0
    glEnable(GL_COLOR_MATERIAL)  # Habilitar el material basado en colores

    # Configuración de la luz
    light_pos = [1.0, 1.0, 1.0, 0.0]  # Posición de la luz
    light_ambient = [0.2, 0.2, 0.2, 1.0]  # Luz ambiental
    light_diffuse = [0.8, 0.8, 0.8, 1.0]  # Luz difusa
    light_specular = [1.0, 1.0, 1.0, 1.0]  # Luz especular

    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

    # Configuración del material
    material_specular = [1.0, 1.0, 1.0, 1.0]
    material_shininess = [50.0]
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, material_shininess)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_TEXTURE_2D)
    
    # Crear un objeto cuadrático
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)  # Habilitar texturas para el objeto
    gluQuadricNormals(quadric, GLU_SMOOTH)
    
    glBindTexture(GL_TEXTURE_2D, texture_id)  # Enlazar la textura cargada
    
    # Dibujar la esfera pequeña
    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)  #  no altere la textura
    glTranslatef(0.0, 0.0, -5.0)  # Mover la esfera para que sea visible
    gluSphere(quadric, 0.5, 32, 32)  # Esfera con radio 0.5
    glPopMatrix()
    
    gluDeleteQuadric(quadric)  # Liberar el recurso del cuadrático
    glDisable(GL_TEXTURE_2D)
    glutSwapBuffers()

def reshape(width, height):
    if height == 0:
        height = 1
    aspect = width / height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, aspect, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    global texture_id
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Esfera con textura e iluminación")
    
    glEnable(GL_DEPTH_TEST)  # Habilitar prueba de profundidad
    texture_id = load_texture("/home/likcos/Materias/Graficacion/code/tex1.png")
    
    init_lighting()  # Inicializar iluminación
    
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMainLoop()

if __name__ == "__main__":
    main()