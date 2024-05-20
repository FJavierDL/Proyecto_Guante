import tkinter as tk
import serial
import numpy as np
from tkinter import messagebox
from PIL import Image, ImageTk
from tensorflow.keras.models import load_model

class Interfaz:
    def __init__(self, master):
        self.master = master
        master.title("Proyecto Guantazo")
        master.geometry("1000x600")
        master.iconbitmap(r'Fotos/foto_mano_ventana.ico')
        self.create_variables()
        self.create_text_boxes()
        self.create_image_frame()
        self.create_buttons()
        self.load_model()

    def create_variables(self):
        self.w1 = tk.DoubleVar()
        self.x1 = tk.DoubleVar()
        self.y1 = tk.DoubleVar()
        self.z1 = tk.DoubleVar()
        self.w2 = tk.DoubleVar()
        self.x2 = tk.DoubleVar()
        self.y2 = tk.DoubleVar()
        self.z2 = tk.DoubleVar()
        self.prediction = tk.StringVar()
        self.max_position = tk.StringVar()
        self.read_count = 0

    def create_text_boxes(self):
        main_frame = tk.Frame(self.master)
        main_frame.pack(side="left", padx=20, pady=10)

        frame1 = tk.Frame(main_frame)
        frame1.pack(side="top", padx=10, pady=10)

        frame2 = tk.Frame(main_frame)
        frame2.pack(side="top", padx=10, pady=10)

        text_boxes1 = [("W1:", self.w1), ("X1:", self.x1), ("Y1:", self.y1), ("Z1:", self.z1)]
        for text, variable in text_boxes1:
            row = tk.Frame(frame1)
            row.pack(side="top", anchor="w", pady=2)
            label = tk.Label(row, text=text, font=("Arial", 12))
            label.pack(side="left")
            text_box = tk.Label(row, textvariable=variable, font=("Arial", 12))
            text_box.pack(side="left", padx=5, pady=2)

        text_boxes2 = [("W2:", self.w2), ("X2:", self.x2), ("Y2:", self.y2), ("Z2:", self.z2)]
        for text, variable in text_boxes2:
            row = tk.Frame(frame2)
            row.pack(side="top", anchor="w", pady=2)
            label = tk.Label(row, text=text, font=("Arial", 12))
            label.pack(side="left")
            text_box = tk.Label(row, textvariable=variable, font=("Arial", 12))
            text_box.pack(side="left", padx=5, pady=2)

        prediction_frame = tk.Frame(main_frame)
        prediction_frame.pack(side="top", padx=10, pady=10)

        predictions = [("Predicción:", self.prediction), ("Gesto:", self.max_position)]
        for text, variable in predictions:
            row = tk.Frame(prediction_frame)
            row.pack(side="top", anchor="w", pady=2)
            label = tk.Label(row, text=text, font=("Arial", 12))
            label.pack(side="left")
            text_box = tk.Label(row, textvariable=variable, font=("Arial", 12))
            text_box.pack(side="left", padx=5, pady=2)

    def create_image_frame(self):
        self.image_frame = tk.Frame(self.master, width=400, height=400)
        self.image_frame.pack(side="right", padx=20, pady=20)
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

    def create_buttons(self):
        button_frame = tk.Frame(self.master)
        button_frame.pack(side="bottom", pady=20)
        self.connect_button = tk.Button(button_frame, text="Conectar", command=self.connect_serial)
        self.connect_button.pack(side="left", padx=(20, 10), pady=10)
        self.disconnect_button = tk.Button(button_frame, text="Desconectar", command=self.disconnect_serial, state=tk.DISABLED)
        self.disconnect_button.pack(side="left", padx=(0, 20), pady=10)

    def display_image(self, max_position):
        images = [Image.open("Fotos/gesto_0.jpeg"), 
                  Image.open("Fotos/gesto_1.jpeg"),
                  Image.open("Fotos/gesto_2.jpeg"),
                  Image.open("Fotos/gesto_3.jpg")]

        photo = ImageTk.PhotoImage(images[max_position].resize((400, 400)))
        self.image_label.configure(image=photo)
        self.image_label.image = photo

    def load_model(self):
        try:
            self.model = load_model("modelo_11_precision_100_4_gestos.h5")
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
        return 0

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
                    self.master.after(100, self.read_serial)
                else:
                    self.process_data(data)
                    self.master.after(100, self.read_serial)
            except serial.SerialException as e:
                messagebox.showerror("Error", f"Error en la comunicación con el puerto serie: {e}")
        else:
            messagebox.showinfo("Información", "El puerto serie no está conectado")

    def process_data(self, data):
        if len(data) == 8:
            self.w1.set(float(data[0]))
            self.x1.set(float(data[1]))
            self.y1.set(float(data[2]))
            self.z1.set(float(data[3]))
            self.w2.set(float(data[4]))
            self.x2.set(float(data[5]))
            self.y2.set(float(data[6]))
            self.z2.set(float(data[7]))
            if self.model:
                input_data = np.array([[float(data[0]), float(data[1]), float(data[2]), float(data[3]),
                                        float(data[4]), float(data[5]), float(data[6]), float(data[7])]])
                prediction = self.model.predict(input_data, verbose=0)
                pred = [np.round(valor * 100, 2) for valor in prediction[0]]
                self.prediction.set(str(pred))
                max_position = prediction.argmax()
                self.max_position.set(str(max_position))
                self.display_image(max_position)
        else:
            messagebox.showerror("Error", "Los datos recibidos no tienen el formato correcto")

def main():
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()

if __name__ == "__main__":  
    main()
