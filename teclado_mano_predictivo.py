import cv2
import mediapipe as mp
import numpy as np
import time
from transformers import pipeline
# Inicializa GPT-2 para predicción de texto
modelo = pipeline("text-generation", model="distilgpt2")

# Inicializa MediaPipe para la mano
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

# Teclado: letras, números, espacio y borrar
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
sugerencias = []

def dibujar_teclado(frame, seleccion):
    h, w, _ = frame.shape
    x_inicio = (w - len(teclas[0]) * tamaño_celda) // 2
    y_inicio = h - len(teclas) * tamaño_celda - 100

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
    y_inicio = h - len(teclas) * tamaño_celda - 100

    j = (x - x_inicio) // tamaño_celda
    i = (y - y_inicio) // tamaño_celda

    if 0 <= i < len(teclas) and 0 <= j < len(teclas[i]):
        return (i, j)
    return None

def obtener_sugerencias(texto):
    try:
        resultado = modelo(texto, max_length=len(texto) + 6, num_return_sequences=1)
        sugerencia = resultado[0]["generated_text"][len(texto):].strip().split(" ")[0]
        return [sugerencia]
    except:
        return []

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
            puntos = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]
            x_coords = [p[0] for p in puntos]
            y_coords = [p[1] for p in puntos]
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 255), 2)

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
                        sugerencias = obtener_sugerencias(texto_escrito)
                        tiempo_seleccion = time.time()
                else:
                    seleccion_previa = seleccion
                    tiempo_seleccion = time.time()

    cv2.putText(frame, texto_escrito, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2)

    for i, sugerencia in enumerate(sugerencias[:3]):
        cv2.putText(frame, f"{i+1}. {sugerencia}", (30, 90 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 180), 2)

    dibujar_teclado(frame, seleccion)
    cv2.imshow("Teclado Mano + GPT-2", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()