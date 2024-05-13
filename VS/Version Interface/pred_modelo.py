# Archivo 1: prediccion_modelo.py
from tensorflow.keras.models import load_model
import numpy as np

modelo = None

def carga_modelo():
    global modelo
    try:
        modelo = load_model("modelo_3_precision_99,906_porc_sigmoid_2_neuronas_intermedia.h5")
        print("Modelo cargado correctamente")
    except Exception as e:
        print("Error al cargar el modelo:", e)

def predice(datos):
    if modelo is not None:
        datos = [float(dato) for dato in datos.split(',')]
        datos = np.expand_dims(datos, axis=0)
        prediccion_modelo = modelo.predict(datos)
        prediccion = np.hstack((datos, prediccion_modelo))
        return prediccion
    else:
        print("Error: El modelo no ha sido cargado correctamente")

def parsea(pred):
    prediccion = pred[0][4:]
    posicion = prediccion.argmax()
    print(f"El gesto es el tipo {posicion}")
    return posicion
