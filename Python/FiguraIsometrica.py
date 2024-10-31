import numpy as np
import cv2

# Ventana
width, height = 400, 400
background_color = (255, 255, 255)
line_color = (0, 0, 0)
line_thickness = 2

# Fondo
image = np.ones((height, width, 3), dtype=np.uint8) * 255

# Definir los vértices de las bases hexagonales en 3D
# Base inferior (z = -1) y base superior (z = 1)
hex_base_bottom = []
hex_base_top = []
for i in range(6):
    angle = np.radians(60 * i)
    x = np.cos(angle)
    y = np.sin(angle)
    hex_base_bottom.append([x, y, -1])
    hex_base_top.append([x, y, 1])

# Combinar las dos bases
prism_vertices = np.array(hex_base_bottom + hex_base_top)

# Matriz de proyección isométrica
angle = np.radians(30)
iso_matrix = np.array([
    [np.cos(angle), 0, -np.cos(angle)],
    [np.sin(angle), 1, np.sin(angle)]
])

# Escala y desplazamiento de los puntos 2D
scale = 80  # Escalar para hacerlo visible en la imagen
offset = np.array([width // 2, height // 2])  # Centrar el prisma en la imagen

# Proyectar los puntos 3D en el plano 2D
prism_2d = []
for vertex in prism_vertices:
    point_2d = iso_matrix @ vertex[:3] * scale + offset
    prism_2d.append(point_2d.astype(int))

# Definir las aristas del prisma
edges = [
    # Conexiones de la base inferior (hexágono inferior)
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0),
    # Conexiones de la base superior (hexágono superior)
    (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 6),
    # Conexiones verticales entre las bases
    (0, 6), (1, 7), (2, 8), (3, 9), (4, 10), (5, 11)
]

# Dibujar las aristas del prisma en la imagen
for edge in edges:
    pt1 = tuple(prism_2d[edge[0]])
    pt2 = tuple(prism_2d[edge[1]])
    cv2.line(image, pt1, pt2, line_color, line_thickness)

# Mostrar la imagen
cv2.imshow("Prisma Hexagonal Isométrico", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
