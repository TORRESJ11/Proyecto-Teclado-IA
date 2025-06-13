import pickle

# Cargar el modelo entrenado
with open("modelo_trigramas.pkl", "rb") as f:
    modelo = pickle.load(f)

# Imprimir claves y predicciones ordenadas por frecuencia
for clave, siguientes in modelo.items():
    print(f"{clave} => {sorted(siguientes.items(), key=lambda item: item[1], reverse=True)}")