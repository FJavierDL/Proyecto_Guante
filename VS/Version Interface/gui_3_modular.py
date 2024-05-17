import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import serial
from tensorflow.keras.models import load_model
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SerialReaderApp:
    def __init__(self, master):
        self.master = master
        master.title("Proyecto Guantazo")
        master.geometry("1600x800")
        master.iconbitmap(r'Fotos/foto_mano_ventana.ico')
        self.create_variables()
        self.create_text_boxes()
        self.create_graph_frames()
        self.create_image_frame()
        self.create_buttons()
        self.load_model()
        self.set_font_size()

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
        # Crear un marco principal para los bloques
        main_frame = tk.Frame(self.master)
        main_frame.pack(side="left", padx=20, pady=10)

        # Crear dos marcos para los dos bloques de variables
        frame1 = tk.Frame(main_frame)
        frame1.pack(side="top", padx=10, pady=10)

        frame2 = tk.Frame(main_frame)
        frame2.pack(side="top", padx=10, pady=10)

        # Definir los cuadros de texto y etiquetas para el primer bloque
        text_boxes1 = [("W1:", self.w1), ("X1:", self.x1), ("Y1:", self.y1), ("Z1:", self.z1)]
        for text, variable in text_boxes1:
            row = tk.Frame(frame1)
            row.pack(side="top", anchor="w", pady=2)
            label = tk.Label(row, text=text, font=("Arial", 12))
            label.pack(side="left")
            text_box = tk.Label(row, textvariable=variable, font=("Arial", 12))
            text_box.pack(side="left", padx=5, pady=2)

        # Definir los cuadros de texto y etiquetas para el segundo bloque
        text_boxes2 = [("W2:", self.w2), ("X2:", self.x2), ("Y2:", self.y2), ("Z2:", self.z2)]
        for text, variable in text_boxes2:
            row = tk.Frame(frame2)
            row.pack(side="top", anchor="w", pady=2)
            label = tk.Label(row, text=text, font=("Arial", 12))
            label.pack(side="left")
            text_box = tk.Label(row, textvariable=variable, font=("Arial", 12))
            text_box.pack(side="left", padx=5, pady=2)

        # Crear un marco para las predicciones
        prediction_frame = tk.Frame(main_frame)
        prediction_frame.pack(side="top", padx=10, pady=10)

        # Cuadros de texto y etiquetas para las predicciones
        predictions = [("Predicción:", self.prediction), ("Posición del máximo:", self.max_position)]
        for text, variable in predictions:
            row = tk.Frame(prediction_frame)
            row.pack(side="top", anchor="w", pady=2)
            label = tk.Label(row, text=text, font=("Arial", 12))
            label.pack(side="left")
            text_box = tk.Label(row, textvariable=variable, font=("Arial", 12))
            text_box.pack(side="left", padx=5, pady=2)

    def create_graph_frames(self):
        graph_frame_container = tk.Frame(self.master)
        graph_frame_container.pack(side="left", padx=20, pady=20)
        
        self.graph_frame1 = tk.Frame(graph_frame_container, width=400, height=400)
        self.graph_frame1.pack(side="top", padx=20, pady=20)

        self.graph_frame2 = tk.Frame(graph_frame_container, width=400, height=400)
        self.graph_frame2.pack(side="top", padx=20, pady=20)

    def create_image_frame(self):
        self.image_frame = tk.Frame(self.master, width=600, height=600)
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
        photo = ImageTk.PhotoImage(images[max_position].resize((600, 600)))
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
                self.prediction.set(str(prediction))
                max_position = prediction.argmax()
                self.max_position.set(str(max_position))
                self.display_image(max_position)
                self.update_graphs()
        else:
            messagebox.showerror("Error", "Los datos recibidos no tienen el formato correcto")

    def update_graphs(self):
        # Datos para los gráficos
        data1 = [self.w1.get(), self.x1.get(), self.y1.get(), self.z1.get()]
        data2 = [self.w2.get(), self.x2.get(), self.y2.get(), self.z2.get()]
        labels = ['W', 'X', 'Y', 'Z']

        # Crear el primer gráfico
        fig1 = Figure(figsize=(4, 4), dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.bar(labels, data1, color='blue')
        ax1.set_title('Valores de W1, X1, Y1, Z1')

        # Crear el segundo gráfico
        fig2 = Figure(figsize=(4, 4), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.bar(labels, data2, color='green')
        ax2.set_title('Valores de W2, X2, Y2, Z2')

        # Limpiar los marcos anteriores
        for widget in self.graph_frame1.winfo_children():
            widget.destroy()
        for widget in self.graph_frame2.winfo_children():
            widget.destroy()

        # Agregar los gráficos a los marcos correspondientes
        canvas1 = FigureCanvasTkAgg(fig1, master=self.graph_frame1)
        canvas1.draw()
        canvas1.get_tk_widget().pack()

        canvas2 = FigureCanvasTkAgg(fig2, master=self.graph_frame2)
        canvas2.draw()
        canvas2.get_tk_widget().pack()

    def set_font_size(self):
        self.master.option_add('*Font', 'Arial 12')

def main():
    root = tk.Tk()
    app = SerialReaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

