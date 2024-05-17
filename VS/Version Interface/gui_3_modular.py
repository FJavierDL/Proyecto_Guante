import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import serial
from tensorflow.keras.models import load_model

class SerialReaderApp:
    def __init__(self, master):
        self.master = master
        master.title("Proyecto Guantazo")
        master.geometry("1200x500")
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
        text_boxes = [("W1:", self.w1, 0), ("X1:", self.x1, 1), ("Y1:", self.y1, 2), ("Z1:", self.z1, 3), 
                    ("W2:", self.w2, 4), ("X2:", self.x2, 5), ("Y2:", self.y2, 6), ("Z2:", self.z2, 7),
                    ("Predicción:", self.prediction, 8), ("Posición del máximo:", self.max_position, 9)]
        for text, variable, row in text_boxes:
            label = tk.Label(self.master, text=text)
            label.pack(side="left", padx=(20, 10), pady=10)
            text_box = tk.Label(self.master, textvariable=variable)
            text_box.pack(side="left", padx=(0, 20), pady=10)

    def create_image_frame(self):
        self.image_frame = tk.Frame(self.master, width=200, height=200)
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
        images = [Image.open("Fotos/gesto_0.jpeg"), Image.open("Fotos/gesto_1.jpeg")]
        photo = ImageTk.PhotoImage(images[max_position].resize((300, 300)))
        self.image_label.configure(image=photo)
        self.image_label.image = photo
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")


    def load_model(self):
        try:
            self.model = load_model("modelo_7_precision_98,9487_4_gestos.h5")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el modelo: {e}")
            self.model = None

    def connect_serial(self):
        # try:
        #     self.ser = serial.Serial('COM5', 115200, timeout=1)
        #     self.connect_button.config(state=tk.DISABLED)
        #     self.disconnect_button.config(state=tk.NORMAL)
        #     self.read_serial()
        # except serial.SerialException as e:
        #     messagebox.showerror("Error", f"Error al conectar al puerto serie: {e}")
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
                    self.master.after(100, self.read_serial)  # Saltar la lectura
                else:
                    self.process_data(data)
                    self.master.after(100, self.read_serial)  # Leer cada 100ms
            except serial.SerialException as e:
                messagebox.showerror("Error", f"Error en la comunicación con el puerto serie: {e}")
        else:
            messagebox.showinfo("Información", "El puerto serie no está conectado")

    def process_data(self, data):
        print(len(data))
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
                prediction = self.model.predict([[float(data[0]), float(data[1]), float(data[2]), float(data[3]),
                                                float(data[4]), float(data[5]), float(data[6]), float(data[7])]], verbose=0)
                print(prediction)
                self.prediction.set(str(prediction))
                max_position = prediction.argmax()
                self.max_position.set(str(max_position))
                self.display_image(max_position)
        else:
            messagebox.showerror("Error", "Los datos recibidos no tienen el formato correcto")

    def display_image(self, max_position):
        images = [Image.open("Fotos/gesto_0.jpeg"), Image.open("Fotos/gesto_1.jpeg")]
        photo = ImageTk.PhotoImage(images[max_position].resize((300, 300)))
        self.image_label.configure(image=photo)
        self.image_label.image = photo


def main():
    root = tk.Tk()
    # icono = tk.PhotoImage(file="Fotos/foto mano ventana.avif")
    # root.iconphoto(True, icono)
    app = SerialReaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
