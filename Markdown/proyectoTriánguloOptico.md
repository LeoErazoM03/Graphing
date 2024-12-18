```python
import numpy as np
import cv2 as cv
import math

cap = cv.VideoCapture(0)

# Parámetros para flujo óptico
lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

_, vframe = cap.read()
vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)

# Puntos para las transformaciones
p0 = np.array([
    (50, 50),    # Rotar sentido horario
    (50, 400),   # Rotar sentido antihorario
    (300, 50),   # Trasladar arriba
    (300, 400),  # Trasladar abajo
    (590, 50),   # Trasladar a la derecha
    (50, 200),   # Trasladar a la izquierda
    (590, 200),  # Aumentar tamaño
    (590, 400),  # Disminuir tamaño
])
p0 = np.float32(p0[:, np.newaxis, :])

mask = np.zeros_like(vframe)

# Variables geométricas
centro = [300, 300]
size = 100
angulo = 0
escala = 1.0

# Funciones de transformación
def redibujo(frame, centro, size, angulo, escala):
    cx, cy = centro
    altura = size * escala

    # Coordenadas de un hexágono regular
    puntos = [
        (cx + altura * math.cos(math.radians(60 * i + angulo)),
         cy + altura * math.sin(math.radians(60 * i + angulo)))
        for i in range(6)
    ]

    # Convertir a enteros
    puntos = np.array([[int(x), int(y)] for x, y in puntos], np.int32)
    puntos = puntos.reshape((-1, 1, 2))

    # Dibujar el hexágono relleno
    cv.fillPoly(frame, [puntos], (255, 0, 0))

def rotar(x, y, cx, cy, theta):
    x_new = cx + (x - cx) * math.cos(theta) - (y - cy) * math.sin(theta)
    y_new = cy + (x - cx) * math.sin(theta) + (y - cy) * math.cos(theta)
    return int(x_new), int(y_new)

# Bucle principal
while True:
    _, frame = cap.read()
    frame = cv.flip(frame, 1)
    fgris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    ventana_triangulo = np.zeros((600, 600, 3), dtype=np.uint8)

    # Calcular flujo óptico
    p1, st, err = cv.calcOpticalFlowPyrLK(vgris, fgris, p0, None, **lk_params)

    # Mantener los puntos fijos
    if p1 is None:
        p1 = p0

    bp1 = p1[st == 1]
    bp0 = p0[st == 1]

    for i, (nv, vj) in enumerate(zip(bp1, bp0)):
        a, b = (int(x) for x in nv.ravel())
        c, d = (int(x) for x in vj.ravel())
        dist = np.linalg.norm(nv.ravel() - vj.ravel())

        # Casos de movimiento
        if dist > 30: 
            if i == 0:  # Rotar sentido horario
                angulo += 10
            elif i == 1:  # Rotar sentido antihorario
                angulo -= 10
            elif i == 2:  # Trasladar arriba
                centro[1] -= 10
            elif i == 3:  # Trasladar abajo
                centro[1] += 10
            elif i == 4:  # Trasladar a la derecha
                centro[0] += 10
            elif i == 5:  # Trasladar a la izquierda
                centro[0] -= 10
            elif i == 6:  # Aumentar tamaño
                escala += 0.1
            elif i == 7:  # Disminuir tamaño
                escala = max(0.1, escala - 0.1)

        # Dibujar flujo óptico
        frame = cv.line(frame, (c, d), (a, b), (0, 0, 255), 2)
        frame = cv.circle(frame, (a, b), 3, (0, 255, 0), -1)

    redibujo(ventana_triangulo, centro, size, angulo, escala)

    vgris = fgris.copy()

    cv.imshow('Camara', frame)
    cv.imshow('Hexagono', ventana_triangulo)

    if cv.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv.destroyAllWindows()

```