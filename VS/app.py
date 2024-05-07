import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from PIL import Image, ImageTk
import random

# Función para generar un nuevo valor
def generar_valor():
    return random.random() * 10  # Valor aleatorio entre 0 y 10

# Función para actualizar los datos del gráfico, cuadro de texto y la imagen
def actualizar_datos(i):
    # Agregar un nuevo valor a la lista
    nuevo_valor = generar_valor()
    nuevos_valores.append(nuevo_valor)

    # Limitar la lista de valores para mostrar solo los últimos 10
    if len(nuevos_valores) > 10:
        nuevos_valores.pop(0)

    # Limpiar el gráfico y volver a graficar los datos actualizados
    ax.clear()
    ax.plot(range(len(nuevos_valores)), nuevos_valores, marker='o')
    ax.set_title('Gráfico en Tiempo Real')
    ax.set_xlabel('Muestras')
    ax.set_ylabel('Valor')
    ax.set_ylim(0, 10)

    # Actualizar el cuadro de texto con el último valor
    texto_actualizado.set(f'Último valor: {nuevo_valor:.2f}')

    # Actualizar la imagen según el valor
    if nuevo_valor > 5:
        img_path = "img1.jpg"  # Ruta de la imagen si el valor es mayor que 5
    else:
        img_path = "img2.jpg"  # Ruta de la imagen si el valor es menor o igual que 5

    img = Image.open(img_path)
    img = img.resize((200, 200))
    photo = ImageTk.PhotoImage(img)
    imagen_label.config(image=photo)
    imagen_label.image = photo

# Crear la ventana de la aplicación
root = tk.Tk()
root.title("Gráfico en Tiempo Real")

# Crear la figura y el eje
fig, ax = plt.subplots()

# Lista para almacenar los nuevos valores
nuevos_valores = []

# Crear el lienzo de matplotlib dentro de la ventana de la aplicación
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Agregar un cuadro de texto
texto_actualizado = tk.StringVar()
texto_actualizado.set('Último valor: 0.00')
texto_label = tk.Label(root, textvariable=texto_actualizado)
texto_label.pack()

# Agregar una imagen inicial
img_path = "img1.jpg"  # Ruta de la imagen inicial
img = Image.open(img_path)
img = img.resize((200, 200))
photo = ImageTk.PhotoImage(img)
imagen_label = tk.Label(root, image=photo)
imagen_label.image = photo
imagen_label.pack()

# Crear la animación
ani = animation.FuncAnimation(fig, actualizar_datos, interval=1000)

# Ejecutar la aplicación
tk.mainloop()
