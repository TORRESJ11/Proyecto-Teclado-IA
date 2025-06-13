import cv2
import mediapipe as mp
import numpy as np
import time

# Configuración de Mediapipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Teclado extendido con números, letras, borrar y espacio
teclas = [
    list("1234567890"),
    list("QWERTYUIOP"),
    list("ASDFGHJKL"),
    list("ZXCVBNM←␣")  # ␣ representa SPACE
]

# Dimensiones
tamaño_celda = 60
margen = 20
ancho_teclado = max(len(fila) for fila in teclas) * tamaño_celda
alto_teclado = len(teclas) * tamaño_celda

# Variables
texto_escrito = ""
tiempo_parpadeo = 0
seleccion_previa = None
tiempo_confirmacion = 1.0  # segundos para confirmar con parpadeo

def dibujar_teclado(frame, tecla_actual):
    h, w, _ = frame.shape
    x_inicio = (w - ancho_teclado) // 2
    y_inicio = h - alto_teclado - 50

    for i, fila in enumerate(teclas):
        for j, tecla in enumerate(fila):
            x = x_inicio + j * tamaño_celda
            y = y_inicio + i * tamaño_celda
            color = (0, 100, 250) if (i, j) == tecla_actual else (50, 50, 50)
            cv2.rectangle(frame, (x, y), (x + tamaño_celda, y + tamaño_celda), color, -1)
            txt = "SPACE" if tecla == "␣" else ("DEL" if tecla == "←" else tecla)
            cv2.putText(frame, txt, (x + 5, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

def detectar_parpadeo(puntos, ojo_ids):
    arriba = puntos[ojo_ids[1]]
    abajo = puntos[ojo_ids[5]]
    distancia = abs(arriba.y - abajo.y)
    return distancia < 0.015

def obtener_tecla_enfocada(punto_iris, h, w):
    x = int(punto_iris.x * w)
    y = int(punto_iris.y * h)
    x_inicio = (w - ancho_teclado) // 2
    y_inicio = h - alto_teclado - 50

    j = (x - x_inicio) // tamaño_celda
    i = (y - y_inicio) // tamaño_celda

    if 0 <= i < len(teclas) and 0 <= j < len(teclas[i]):
        return (i, j)
    return None

# Cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = face_mesh.process(frame_rgb)

    tecla_actual = None
    parpadeo = False

    if resultado.multi_face_landmarks:
        rostro = resultado.multi_face_landmarks[0]
        puntos = rostro.landmark

        iris_derecha = puntos[468]
        tecla_actual = obtener_tecla_enfocada(iris_derecha, h, w)

        parpadeo_d = detectar_parpadeo(puntos, [33, 159, 158, 157, 173, 145])
        parpadeo_i = detectar_parpadeo(puntos, [362, 386, 385, 384, 398, 374])
        parpadeo = parpadeo_d and parpadeo_i

        if tecla_actual:
            if seleccion_previa == tecla_actual:
                if time.time() - tiempo_parpadeo > tiempo_confirmacion and parpadeo:
                    letra = teclas[tecla_actual[0]][tecla_actual[1]]
                    if letra == "←":
                        texto_escrito = texto_escrito[:-1]
                    elif letra == "␣":
                        texto_escrito += " "
                    else:
                        texto_escrito += letra
                    tiempo_parpadeo = time.time()
            else:
                seleccion_previa = tecla_actual
                tiempo_parpadeo = time.time()

    # Mostrar texto
    cv2.putText(frame, texto_escrito, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
    dibujar_teclado(frame, tecla_actual)
    cv2.imshow("Teclado Visual Completo", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()