import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter import font
from datetime import datetime
import getpass
import socket
import time
import random

def generar_numero_aleatorio(n1, n2):
    return random.randint(n1, n2)

def mostrar_imagen_con_texto():
    Host_nombre = socket.gethostname()
    nombre_usuario = getpass.getuser()
    host_y_usuario = f"{Host_nombre} / {nombre_usuario}"
    tiempo_espera = generar_numero_aleatorio(3000, 8000)
    root = tk.Tk()
    root.overrideredirect(True)  # Oculta la barra de título y bordes de la ventana

    # Obtener el ancho y alto de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calcular la posición de la imagen para que aparezca en el centro
    x = (screen_width - 300) // 2  # Ajusta 300 al ancho deseado de la imagen
    y = (screen_height - 300) // 2  # Ajusta 300 al alto deseado de la imagen
    root.geometry("+{}+{}".format(x, y))  # Posición de la ventana

    # Cargar la imagen y cambiar su tamaño
    imagen = Image.open('lib/assets/Images/Holding/Hold.png')  # la ruta desde lib porque el ejecutable se llamara desde afuera y necesita cojer la ruta completa
    imagen = imagen.resize((300, 300))
    draw = ImageDraw.Draw(imagen)

    texto = host_y_usuario
    fuente = ImageFont.truetype("arial.ttf", 10)  # Puedes cambiar "arial.ttf" por otra fuente
    text_bbox = draw.textbbox((0, 0), texto, font=fuente)

    
    # Calcular la posición del texto para que aparezca en el centro
    text_bbox = draw.textbbox((0, 0), texto, font=fuente)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (imagen.width - text_width) // 2
    text_y = (imagen.height - text_height) // 2
    
    # Ajustar la posición del texto con parámetros adicionales
    offset_x = 0  # Cambia este valor para ajustar la posición horizontal
    offset_y = 70  # Cambia este valor para ajustar la posición vertical
    draw.text((text_x + offset_x, text_y + offset_y), texto, fill="white", font=fuente)

    # Crear una referencia global a img en la ventana principal
    root.img = ImageTk.PhotoImage(imagen)

    panel = tk.Label(root, image=root.img)
    panel.pack()

    root.after(tiempo_espera, root.destroy)
    root.mainloop()

# Asegúrate de que la función no se ejecute automáticamente al importar el módulo
if __name__ == "__main__":
    mostrar_imagen_con_texto()