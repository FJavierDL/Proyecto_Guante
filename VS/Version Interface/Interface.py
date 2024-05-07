import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from PIL import Image, ImageTk
import time


import conex_puerto_serie
import prediccion_modelo

global puerto_serie, datos, posicion

def inicializa():
    puerto_serie = conex_puerto_serie.config_puerto_serie()
    prediccion_modelo.carga_modelo()


def usa_modelo():
    cont = 0
    print()
    while cont<50:
        datos = puerto_serie.readline().decode().strip()  # Leer datos de la UART
        print(datos, end='\r')

        prediccion = prediccion_modelo.predice(datos)
        print(prediccion)
        posicion = prediccion_modelo.parsea(prediccion)

        time.sleep(0.001)
        cont+=1

    puerto_serie.close()    # Cerrar el puerto serie


# Función para actualizar los datos del gráfico, cuadro de texto y la imagen
def actualizar_datos(i):
    # Agregar un nuevo valor a la lista
    nuevo_valor = datos
    x.append(nuevo_valor[0][0])
    y.append(nuevo_valor[0][1])
    z.append(nuevo_valor[0][2])

    # Limitar la lista de valores para mostrar solo los últimos 10
    if len(nuevo_valor) > 20:
        nuevo_valor.pop(0)

    # Limpiar el gráfico y volver a graficar los datos actualizados
    ax.clear()
    ax.plot(range(len(x)), x, marker='x')
    ax.plot(range(len(y)), y, marker='y')
    ax.plot(range(len(z)), z, marker='z')
    ax.set_title('Gráfico en Tiempo Real')
    ax.set_xlabel('Muestras')
    ax.set_ylabel('Valor')
    ax.set_ylim(0, 20)

    # Actualizar el cuadro de texto con el último valor
    texto_actualizado.set(f'El gesto es: {posicion}')

    # Actualizar la imagen según el valor
    if posicion == 1:
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

inicializa()

# Crear la figura y el eje
fig, ax = plt.subplots()

# Lista para almacenar los nuevos valores
x,y,z = [],[],[]


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
ani = animation.FuncAnimation(fig, actualizar_datos(), interval=1000)

usa_modelo()

# Ejecutar la aplicación
tk.mainloop()
