from tensorflow.keras.models import load_model
import numpy as np

modelo = None  # Inicializa modelo como None

def carga_modelo():
    global modelo  # Indica que se utilizará la variable global 'modelo' dentro de esta función
    try:
        modelo = load_model("modelo_3_precision_99,906_porc_sigmoid_2_neuronas_intermedia.h5")
        print("Modelo cargado correctamente")
        print(modelo)  # Imprime el modelo para verificar que se haya cargado correctamente
    except Exception as e:
        print("Error al cargar el modelo:", e)

def predice(datos):
    prediccion = []
    datos = np.array(datos)
    datos = np.expand_dims(datos, axis=0)  # Agregar una dimensión adicional para representar el lote de datos
    if modelo is not None:
        prediccion_modelo = modelo.predict(datos)
        prediccion = np.hstack((datos, prediccion_modelo))  # Concatenar horizontalmente los datos originales y la predicción del modelo
    else:
        print("Error: El modelo no ha sido cargado correctamente")
    return prediccion

def parsea(pred):
    prediccion = pred[0][4:]
    prediccion = list(prediccion)
    posicion = prediccion.index(max(prediccion))
    print(f"El gesto es el tipo {posicion}")
    return posicion