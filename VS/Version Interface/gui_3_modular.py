import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import serial
from tensorflow.keras.models import load_model

class SerialReaderApp:
    def __init__(self, master):
        self.master = master
        master.title("Serial Reader")
        master.geometry("1200x500")
        self.create_variables()
        self.create_text_boxes()
        self.create_image_frame()
        self.create_buttons()
        self.load_model()

    def create_variables(self):
        self.w = tk.DoubleVar()
        self.x = tk.DoubleVar()
        self.y = tk.DoubleVar()
        self.z = tk.DoubleVar()
        self.prediction = tk.StringVar()
        self.max_position = tk.StringVar()
        self.read_count = 0

    def create_text_boxes(self):
        text_boxes = [("W:", self.w, 0), ("X:", self.x, 1), ("Y:", self.y, 2), ("Z:", self.z, 3), 
                    ("Predicción:", self.prediction, 4), ("Posición del máximo:", self.max_position, 5)]
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
            self.model = load_model("modelo_3_precision_99,906_porc_sigmoid_2_neuronas_intermedia.h5")
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
    app = SerialReaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
