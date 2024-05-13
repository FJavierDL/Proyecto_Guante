import tkinter as tk
from PIL import Image, ImageTk
import serial

class InterfazGrafica(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interfaz Gráfica")
        self.geometry("1200x700")

        # Centrar la ventana en la pantalla
        self.center_window()

        # Configurar el puerto serie
        self.puerto_serie = serial.Serial('COM5', 115200)

        # Rutas de las fotos
        self.img_paths = ["Fotos\\img1.jpg", "Fotos\\img2.jpg"]  

        # Botón para cambiar la foto
        self.cambiar_foto_boton = tk.Button(self, text="Cambiar Foto", command=self.cambiar_foto, width=15, height=3)
        self.cambiar_foto_boton.grid(row=0, column=0, padx=20, pady=20)

        # Variables w, x, y, z
        self.w = tk.DoubleVar(value=0.0)
        self.x = tk.DoubleVar(value=0.0)
        self.y = tk.DoubleVar(value=0.0)
        self.z = tk.DoubleVar(value=0.0)

        w_label = tk.Label(self, text="W:")
        w_label.grid(row=1, column=0, padx=20, pady=20)
        self.valor_label_w = tk.Label(self, textvariable=self.w, font=("Arial", 24))
        self.valor_label_w.grid(row=1, column=1, padx=20, pady=20)

        x_label = tk.Label(self, text="X:")
        x_label.grid(row=1, column=2, padx=20, pady=20)
        self.valor_label_x = tk.Label(self, textvariable=self.x, font=("Arial", 24))
        self.valor_label_x.grid(row=1, column=3, padx=20, pady=20)

        y_label = tk.Label(self, text="Y:")
        y_label.grid(row=2, column=0, padx=20, pady=20)
        self.valor_label_y = tk.Label(self, textvariable=self.y, font=("Arial", 24))
        self.valor_label_y.grid(row=2, column=1, padx=20, pady=20)

        z_label = tk.Label(self, text="Z:")
        z_label.grid(row=2, column=2, padx=20, pady=20)
        self.valor_label_z = tk.Label(self, textvariable=self.z, font=("Arial", 24))
        self.valor_label_z.grid(row=2, column=3, padx=20, pady=20)

        # Cuadro para mostrar la foto
        self.current_img_index = 0  
        self.load_image()
        self.imagen_label = tk.Label(self, image=self.photo)
        self.imagen_label.grid(row=3, column=0, columnspan=4, padx=20, pady=20)

        # Botón para cerrar la ventana
        self.cerrar_boton = tk.Button(self, text="Cerrar", command=self.cerrar, width=15, height=3)
        self.cerrar_boton.grid(row=4, column=0, padx=20, pady=20, columnspan=4)

        # Configurar el sistema de rejilla para que los elementos se expandan
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

        # Leer datos del puerto serie
        self.leer_puerto_serie()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def load_image(self):
        img_path = self.img_paths[self.current_img_index]
        img = Image.open(img_path)
        img = img.resize((400, 400))
        self.photo = ImageTk.PhotoImage(img)

    def cambiar_foto(self):
        # Cambiar a la siguiente foto en la lista
        self.current_img_index = (self.current_img_index + 1) % len(self.img_paths)
        self.load_image()
        self.imagen_label.config(image=self.photo)

    def cerrar(self):
        # Cerrar el puerto serie
        self.puerto_serie.close()
        # Cerrar la ventana
        self.destroy()

    def leer_puerto_serie(self):
        while True:
            try:
                data = self.puerto_serie.readline().decode().strip()
                partes = data.split(",")  # Dividir la cadena por comas solamente
                valores = [float(part.strip()) for part in partes]
                if len(valores) == 4:
                    self.w.set(valores[0])
                    self.x.set(valores[1])
                    self.y.set(valores[2])
                    self.z.set(valores[3])
            except serial.SerialException:
                print("Error al leer del puerto serie")


if __name__ == "__main__":
    app = InterfazGrafica()
    app.mainloop()
