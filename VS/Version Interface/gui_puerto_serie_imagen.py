import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import serial
import tensorflow as tf
from tensorflow.keras.models import load_model

class SerialReaderApp:
    def __init__(self, master):
        self.master = master
        master.title("Serial Reader")
        master.geometry("1200x500")

        # Variables para almacenar los datos del puerto serie y la predicción
        self.w = tk.DoubleVar()
        self.x = tk.DoubleVar()
        self.y = tk.DoubleVar()
        self.z = tk.DoubleVar()
        self.prediction = tk.StringVar()
        self.max_position = tk.StringVar()

        # Contador para las lecturas del puerto serie
        self.read_count = 0

        # Cuadros de texto para mostrar los datos
        tk.Label(master, text="W:").grid(row=0, column=0, pady=10)
        tk.Label(master, textvariable=self.w).grid(row=0, column=1, pady=10)
        tk.Label(master, text="X:").grid(row=1, column=0, pady=10)
        tk.Label(master, textvariable=self.x).grid(row=1, column=1, pady=10)
        tk.Label(master, text="Y:").grid(row=2, column=0, pady=10)
        tk.Label(master, textvariable=self.y).grid(row=2, column=1, pady=10)
        tk.Label(master, text="Z:").grid(row=3, column=0, pady=10)
        tk.Label(master, textvariable=self.z).grid(row=3, column=1, pady=10)

        # Cuadro de texto para mostrar la predicción
        tk.Label(master, text="Predicción:").grid(row=4, column=0, pady=10)
        tk.Label(master, textvariable=self.prediction).grid(row=4, column=1, pady=10)

        # Cuadro de texto para mostrar la posición del máximo
        tk.Label(master, text="Posición del máximo:").grid(row=5, column=0, pady=10)
        tk.Label(master, textvariable=self.max_position).grid(row=5, column=1, pady=10)

        # Imagen
        self.image_frame = tk.Frame(master, width=200, height=200)
        self.image_frame.grid(row=0, column=2, rowspan=4, padx=10)

        # Cargar imágenes
        self.image1 = Image.open("Fotos/gesto_0.jpeg")
        self.image2 = Image.open("Fotos/gesto_1.jpeg")

        # Etiquetas para mostrar las imágenes
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

        # Botones para conectar y desconectar
        self.connect_button = tk.Button(master, text="Conectar", command=self.connect_serial)
        self.connect_button.grid(row=6, column=0, pady=10)
        self.disconnect_button = tk.Button(master, text="Desconectar", command=self.disconnect_serial, state=tk.DISABLED)
        self.disconnect_button.grid(row=6, column=1, pady=10)
        
        # Cargar el modelo de IA entrenado
        try:
            self.model = load_model("modelo_3_precision_99,906_porc_sigmoid_2_neuronas_intermedia.h5")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el modelo: {e}")
            self.model = None

    def connect_serial(self):
        try:
            self.ser = serial.Serial('COM5', 115200, timeout=1)
            self.connect_button.config(state=tk.DISABLED)
            self.disconnect_button.config(state=tk.NORMAL)
            self.read_serial()
        except serial.SerialException as e:
            messagebox.showerror("Error", f"Error al conectar al puerto serie: {e}")

    def disconnect_serial(self):
        if hasattr(self, 'ser'):
            self.ser.close()
            self.connect_button.config(state=tk.NORMAL)
            self.disconnect_button.config(state=tk.DISABLED)

    def read_serial(self):
        if hasattr(self, 'ser') and self.ser.is_open:
            try:
                data = self.ser.readline().decode('utf-8').strip().split(',')
                if self.read_count < 5:
                    self.read_count += 1
                    self.master.after(100, self.read_serial)  # Saltar la lectura
                else:
                    if len(data) == 4:
                        self.w.set(float(data[0]))
                        self.x.set(float(data[1]))
                        self.y.set(float(data[2]))
                        self.z.set(float(data[3]))
                        if self.model:
                            prediction = self.model.predict([[float(data[0]), float(data[1]), float(data[2]), float(data[3])]], verbose=0)
                            self.prediction.set(str(prediction))
                            max_position = prediction.argmax()
                            self.max_position.set(str(max_position))

                            # Mostrar imágenes según la posición del máximo
                            if max_position == 0:
                                photo = ImageTk.PhotoImage(self.image1.resize((300, 300)))
                                self.image_label.configure(image=photo)
                                self.image_label.image = photo
                            elif max_position == 1:
                                photo = ImageTk.PhotoImage(self.image2.resize((300, 300)))
                                self.image_label.configure(image=photo)
                                self.image_label.image = photo
                    else:
                        messagebox.showerror("Error", "Los datos recibidos no tienen el formato correcto")
                    self.master.after(100, self.read_serial)  # Leer cada 100ms
            except serial.SerialException as e:
                messagebox.showerror("Error", f"Error en la comunicación con el puerto serie: {e}")
        else:
            messagebox.showinfo("Información", "El puerto serie no está conectado")

def main():
    root = tk.Tk()
    app = SerialReaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
