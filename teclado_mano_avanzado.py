import cv2
import mediapipe as mp
import time
import pygame
import pickle

pygame.init()
click_sound = pygame.mixer.Sound("click.wav")

with open("modelo_trigramas.pkl", "rb") as f:
    modelo_trigramas = pickle.load(f)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

# Teclado
filas = [
    list("QWERTYUIOP"),
    list("ASDFGHJKL"),
    list("ZXCVBNM"),
    ["_", "DEL"],
    list("0123456789")
]

tecla_size = 40
espacio_tecla = 10
texto_escrito = ""
ultima_tecla = None
tiempo_inicio = 0
sugerencia = ""
tecla_actual = None

def detectar_gesto_palma_abierta(landmarks):
    dedos_abiertos = [
        landmarks.landmark[8].y < landmarks.landmark[6].y,
        landmarks.landmark[12].y < landmarks.landmark[10].y,
        landmarks.landmark[16].y < landmarks.landmark[14].y,
        landmarks.landmark[20].y < landmarks.landmark[18].y
    ]
    pulgar_izq = landmarks.landmark[4].x < landmarks.landmark[3].x
    pulgar_der = landmarks.landmark[4].x > landmarks.landmark[3].x
    return all(dedos_abiertos) and (pulgar_izq or pulgar_der)

def detectar_punta_indice(hand_landmarks, width, height):
    x = int(hand_landmarks.landmark[8].x * width)
    y = int(hand_landmarks.landmark[8].y * height)
    return x, y

def predecir_palabra(texto, modelo):
    palabras = texto.strip().split()
    if not palabras:
        return []
    prefijo = palabras[-1].lower()
    opciones = set()
    for clave, siguientes in modelo.items():
        for palabra, _ in siguientes.items():
            if palabra.startswith(prefijo):
                opciones.add(palabra)
    return sorted(opciones)[:3]

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = hands.process(rgb)

    teclas_pos = []
    y_base = 100
    tecla_actual = None

    for fila_idx, fila in enumerate(filas):
        fila_ancho = len(fila) * (tecla_size + espacio_tecla) - espacio_tecla
        x_base = (width - fila_ancho) // 2
        for col_idx, tecla in enumerate(fila):
            ancho = tecla_size
            x = x_base + col_idx * (tecla_size + espacio_tecla)
            y = y_base + fila_idx * (tecla_size + espacio_tecla)
            teclas_pos.append((tecla, (x, y, ancho)))

    if resultado.multi_hand_landmarks:
        for hand_landmarks in resultado.multi_hand_landmarks:
            x, y = detectar_punta_indice(hand_landmarks, width, height)
            cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)

            if detectar_gesto_palma_abierta(hand_landmarks):
                texto_escrito = ""
                sugerencia = ""

            for tecla, (tx, ty, tw) in teclas_pos:
                if tx < x < tx + tw and ty < y < ty + tecla_size:
                    tecla_actual = tecla
                    if ultima_tecla != tecla:
                        ultima_tecla = tecla
                        tiempo_inicio = time.time()
                    elif time.time() - tiempo_inicio > 1:
                        if tecla == "_":
                            texto_escrito += " "
                        elif tecla == "DEL":
                            texto_escrito = texto_escrito[:-1]
                        else:
                            texto_escrito += tecla
                        click_sound.play()
                        ultima_tecla = None
                        sugerencia = ""

    # Dibujar teclado con resaltado
    for tecla, (tx, ty, tw) in teclas_pos:
        color = (240, 240, 240)
        if tecla == tecla_actual:
            color = (255, 255, 150)  # Amarillo
        cv2.rectangle(frame, (tx, ty), (tx + tw, ty + tecla_size), color, -1)
        font_scale = 0.6 if len(tecla) == 1 else 0.5
        texto = " " if tecla == "_" else tecla
        (text_width, _), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)
        text_x = tx + (tw - text_width) // 2
        text_y = ty + int(tecla_size * 0.65)
        cv2.putText(frame, texto, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (50, 50, 50), 2)

    # Mostrar texto
    texto_central = texto_escrito.strip()
    text_color = (0, 50, 200)
    texto_pos_x = max(20, width // 2 - len(texto_central) * 10)
    cv2.putText(frame, texto_central, (texto_pos_x, 50), cv2.FONT_HERSHEY_COMPLEX, 1.2, text_color, 2)

    # Sugerencias
    sugerencia = predecir_palabra(texto_escrito, modelo_trigramas)
    if sugerencia:
        for idx, sug in enumerate(sugerencia):
            sx = 40
            sy = height - 120 + idx * 40
            cv2.rectangle(frame, (sx, sy), (sx + 200, sy + 35), (255, 255, 200), -1)
            cv2.putText(frame, sug, (sx + 5, sy + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
            if resultado.multi_hand_landmarks:
                if sx < x < sx + 200 and sy < y < sy + 35:
                    if ultima_tecla != f"SUG{idx}":
                        ultima_tecla = f"SUG{idx}"
                        tiempo_inicio = time.time()
                    elif time.time() - tiempo_inicio > 1:
                        palabras = texto_escrito.strip().split()
                        if palabras:
                            palabras[-1] = sug
                            texto_escrito = " ".join(palabras) + " "
                            click_sound.play()
                            ultima_tecla = None
                            sugerencia = ""

    cv2.imshow("Teclado Mano Predictivo", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()