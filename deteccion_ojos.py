import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

cap = cv2.VideoCapture(0)

def calcular_direccion(puntos_iris, ojo_extremos):
    if puntos_iris and ojo_extremos:
        iris_x = puntos_iris[0][0]
        left_x = ojo_extremos[0][0]
        right_x = ojo_extremos[1][0]

        medio = (left_x + right_x) / 2

        if iris_x < medio - 10:
            return "IZQUIERDA"
        elif iris_x > medio + 10:
            return "DERECHA"
        else:
            return "CENTRO"
    return "NO DETECTADO"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultados = face_mesh.process(rgb)

    if resultados.multi_face_landmarks:
        for rostro in resultados.multi_face_landmarks:
            puntos = rostro.landmark

            # Ojo derecho
            ojo_derecho_ids = [33, 133]  # Extremos
            iris_derecha_id = 468  # Centro del iris derecho

            ojo_derecho = [(int(puntos[i].x * w), int(puntos[i].y * h)) for i in ojo_derecho_ids]
            iris_derecho = [(int(puntos[iris_derecha_id].x * w), int(puntos[iris_derecha_id].y * h))]

            for x, y in ojo_derecho + iris_derecho:
                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

            direccion = calcular_direccion(iris_derecho, ojo_derecho)
            cv2.putText(frame, f"MIRANDO: {direccion}", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Seguimiento de Ojos", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC para salir
        break

cap.release()
cv2.destroyAllWindows()
