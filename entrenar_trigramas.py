import pickle
from collections import defaultdict

def entrenar_trigramas(archivo_txt, archivo_salida):
    modelo = defaultdict(lambda: defaultdict(int))
    with open(archivo_txt, 'r', encoding='utf-8') as f:
        for linea in f:
            palabras = linea.strip().split()
            for i in range(len(palabras) - 2):
                clave = (palabras[i], palabras[i + 1])
                siguiente = palabras[i + 2]
                modelo[clave][siguiente] += 1

    # Convertir a tipos estándar para que pickle pueda guardarlo
    modelo_final = {k: dict(v) for k, v in modelo.items()}

    with open(archivo_salida, 'wb') as f:
        pickle.dump(modelo_final, f)

# Ejecutar
entrenar_trigramas("corpus.txt", "modelo_trigramas.pkl")