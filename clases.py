import numpy as np
import cv2

# Función para generar un solo punto de la elipse en función del parámetro t
def generar_punto_elipse(a, b, t):
    x = int(a * np.cos(t) + 300)  # Desplazamiento para centrar
    y = int(b * np.sin(t) + 300)
    return (x, y)

# Dimensiones de la imagen
img_width, img_height = 600, 600

# Crear una imagen en blanco
imagen = np.zeros((img_height, img_width, 3), dtype=np.uint8)

# Parámetros de las órbitas elípticas (a, b) y colores de los planetas
orbitales = [
    {"a": 100, "b": 50, "color": (255, 0, 0), "velocidad": 1},    # Órbita 1 (rojo)
    {"a": 150, "b": 75, "color": (0, 255, 0), "velocidad": 1.5},  # Órbita 2 (verde)
    {"a": 200, "b": 100, "color": (0, 0, 255), "velocidad": 0.8}, # Órbita 3 (azul)
    {"a": 250, "b": 125, "color": (255, 255, 0), "velocidad": 2}, # Órbita 4 (amarillo)
    {"a": 300, "b": 150, "color": (255, 165, 0), "velocidad": 0.6}# Órbita 5 (naranja)
]

num_puntos = 1000

# Crear los valores del parámetro t para la animación
t_vals = np.linspace(0, 2 * np.pi, num_puntos)

# Bucle de animación
for i, t in enumerate(t_vals):
    # Crear una nueva imagen en blanco en cada iteración
    imagen = np.zeros((img_height, img_width, 3), dtype=np.uint8)
    
    # Dibujar el "sol" en el centro
    cv2.circle(imagen, (300, 300), radius=40, color=(0, 255, 255), thickness=-1)  # Círculo amarillo (sol)
    
    # Dibujar las órbitas y los puntos (planetas)
    for orbita in orbitales:
        a = orbita["a"]
        b = orbita["b"]
        color = orbita["color"]
        velocidad = orbita["velocidad"]
        
        # Generar el punto en la elipse con velocidad ajustada
        punto = generar_punto_elipse(a, b, t * velocidad)
        
        # Dibujar el planeta con su respectivo color
        cv2.circle(imagen, punto, radius=5, color=color, thickness=-1)
        
        # Dibujar la trayectoria completa de la órbita (opcional)
        for t_tray in t_vals:
            pt_tray = generar_punto_elipse(a, b, t_tray)
            cv2.circle(imagen, pt_tray, radius=1, color=(255, 255, 255), thickness=-1)  # Trayectoria blanca

    # Mostrar la imagen con los planetas moviéndose
    cv2.imshow('Sistema Solar', imagen)
    
    # Controlar la velocidad de la animación (en milisegundos)
    if cv2.waitKey(10) & 0xFF == 27:  # 27 es el código ASCII para 'Esc'
        break  # Salir del bucle si se presiona 'Esc'

# Cerrar la ventana después de la animación o al presionar 'Esc'
cv2.destroyAllWindows()
