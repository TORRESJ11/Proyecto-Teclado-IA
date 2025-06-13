
import cv2
import mediapipe as mp
import numpy as np
import time

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

# Teclas del teclado
teclas = [
    list("1234567890"),
    list("QWERTYUIOP"),
    list("ASDFGHJKL"),
    list("ZXCVBNM←␣")
]

tamaño_celda = 60
texto_escrito = ""
seleccion_previa = None
tiempo_seleccion = 0

def dibujar_teclado(frame, seleccion):
    h, w, _ = frame.shape
    x_inicio = (w - len(teclas[0]) * tamaño_celda) // 2
    y_inicio = h - len(teclas) * tamaño_celda - 50

    for i, fila in enumerate(teclas):
        for j, tecla in enumerate(fila):
            x = x_inicio + j * tamaño_celda
            y = y_inicio + i * tamaño_celda
            color = (0, 255, 0) if (i, j) == seleccion else (50, 50, 50)
            cv2.rectangle(frame, (x, y), (x + tamaño_celda, y + tamaño_celda), color, -1)
            txt = "SPACE" if tecla == "␣" else ("DEL" if tecla == "←" else tecla)
            cv2.putText(frame, txt, (x + 5, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

def obtener_tecla_enfocada(x, y, w, h):
    x_inicio = (w - len(teclas[0]) * tamaño_celda) // 2
    y_inicio = h - len(teclas) * tamaño_celda - 50

    j = (x - x_inicio) // tamaño_celda
    i = (y - y_inicio) // tamaño_celda

    if 0 <= i < len(teclas) and 0 <= j < len(teclas[i]):
        return (i, j)
    return None

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = hands.process(frame_rgb)

    seleccion = None

    if resultado.multi_hand_landmarks:
        for hand_landmarks in resultado.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)
            cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)
            seleccion = obtener_tecla_enfocada(x, y, w, h)

            if seleccion:
                if seleccion == seleccion_previa:
                    if time.time() - tiempo_seleccion > 1.0:
                        letra = teclas[seleccion[0]][seleccion[1]]
                        if letra == "←":
                            texto_escrito = texto_escrito[:-1]
                        elif letra == "␣":
                            texto_escrito += " "
                        else:
                            texto_escrito += letra
                        tiempo_seleccion = time.time()
                else:
                    seleccion_previa = seleccion
                    tiempo_seleccion = time.time()

    cv2.putText(frame, texto_escrito, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2)
    dibujar_teclado(frame, seleccion)
    cv2.imshow("Teclado con Mano", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
