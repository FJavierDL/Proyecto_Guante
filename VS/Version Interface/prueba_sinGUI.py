import serial
import numpy as np
import tensorflow as tf
import time

def load_model(model_path):
    model = tf.keras.models.load_model(model_path)
    return model

def main():
    ser = serial.Serial('COM5', 115200)
    
    model_path = "modelo_11_precision_100_4_gestos.h5"
    model = load_model(model_path)
    
    try:
        for _ in range(30):
            line = ser.readline().decode().strip()
            
            if line and len(line.split(',')) == 8:
                w1, x1, y1, z1, w2, x2, y2, z2 = map(float, line.split(','))
                data = np.array([[w1, x1, y1, z1, w2, x2, y2, z2]])
                
                prediction = model.predict(data, verbose=0)
                
                max_index = np.argmax(prediction)
                print(f"{w1}, {x1}, {y1}, {z1}, {w2}, {x2}, {y2}, {z2}\nPrediccion: {prediction}\nGesto: {max_index}\n\n")
            else:
                print("La línea está vacía o no tiene 4 datos.")
            
    except KeyboardInterrupt:
        print("Programa terminado por el usuario.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
