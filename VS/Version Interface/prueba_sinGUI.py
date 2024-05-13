import serial
import numpy as np
import tensorflow as tf
import time

def load_model(model_path):
    model = tf.keras.models.load_model(model_path)
    return model

def main():
    ser = serial.Serial('COM5', 115200)
    
    model_path = "modelo_3_precision_99,906_porc_sigmoid_2_neuronas_intermedia.h5"
    model = load_model(model_path)
    
    try:
        for _ in range(400):
            line = ser.readline().decode().strip()
            
            if line and len(line.split(',')) == 4:
                w, x, y, z = map(float, line.split(','))
                data = np.array([[w, x, y, z]])
                
                prediction = model.predict(data, verbose=0)
                
                max_index = np.argmax(prediction)
                print(w, ",", x, ",", y, ",", z, "-->", prediction, " --> Gesto:", max_index)
            else:
                print("La línea está vacía o no tiene 4 datos.")
            
    except KeyboardInterrupt:
        print("Programa terminado por el usuario.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
