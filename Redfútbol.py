import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

lkparm = dict(winSize=(15, 15), maxLevel=2,
              criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

_, vframe = cap.read()
vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)

# Define una cuadrícula de puntos, como una red.
p0 = np.array([(100, 100), (200, 100), (300, 100), (400, 100), (500, 100),
               (100, 200), (200, 200), (300, 200), (400, 200), (500, 200),
               (100, 300), (200, 300), (300, 300), (400, 300), (500, 300),
               (100, 400), (200, 400), (300, 400), (400, 400), (500, 400)])

p0 = np.float32(p0[:, np.newaxis, :])

mask = np.zeros_like(vframe)

while True:
    _, frame = cap.read()
    fgris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    p1, st, err = cv.calcOpticalFlowPyrLK(vgris, fgris, p0, None, **lkparm)

    if p1 is None:
        vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)
        p0 = np.array([(100, 100), (200, 100), (300, 100), (400, 100)])
        p0 = np.float32(p0[:, np.newaxis, :])
        mask = np.zeros_like(vframe)
        cv.imshow('ventana', frame)
    else:
        bp1 = p1[st == 1]
        bp0 = p0[st == 1]

        # Dibuja líneas para simular una red (conecta los puntos en la cuadrícula)
        for i, (nv, vj) in enumerate(zip(bp1, bp0)):
            a, b = (int(x) for x in nv.ravel())
            c, d = (int(x) for x in vj.ravel())

            # Dibuja la línea de la posición anterior a la nueva
            frame = cv.line(frame, (c, d), (a, b), (0, 0, 255), 2)
            frame = cv.circle(frame, (c, d), 2, (255, 0, 0), -1)
            frame = cv.circle(frame, (a, b), 3, (0, 255, 0), -1)

            # Conexiones horizontales (evita el último punto de cada fila)
            if (i + 1) % 5 != 0 and i + 1 < len(bp1):  # Conexión horizontal
                a_next, b_next = (int(x) for x in bp1[i + 1].ravel())
                frame = cv.line(frame, (a, b), (a_next, b_next), (0, 255, 0), 1)

            # Conexiones verticales (evita la última fila)
            if i + 5 < len(bp1):  # Conexión vertical
                a_below, b_below = (int(x) for x in bp1[i + 5].ravel())
                frame = cv.line(frame, (a, b), (a_below, b_below), (0, 255, 0), 1)

        cv.imshow('ventana', frame)

        vgris = fgris.copy()

        if (cv.waitKey(1) & 0xff) == 27:
            break

cap.release()
cv.destroyAllWindows()
