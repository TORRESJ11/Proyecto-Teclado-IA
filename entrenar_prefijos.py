import pickle
from collections import defaultdict

def entrenar_modelo_prefijos(archivo_txt):
    modelo = defaultdict(list)
    with open(archivo_txt, 'r', encoding='utf-8') as f:
        for linea in f:
            for palabra in linea.strip().split():
                palabra = palabra.upper()
                for i in range(1, len(palabra) + 1):
                    prefijo = palabra[:i]
                    if palabra not in modelo[prefijo]:
                        modelo[prefijo].append(palabra)

    with open("modelo_prefijos.pkl", "wb") as f:
        pickle.dump(modelo, f)

if __name__ == "__main__":
    entrenar_modelo_prefijos("corpus.txt")