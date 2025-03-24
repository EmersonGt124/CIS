import tkinter as tk
from tkinter import messagebox, Label, PhotoImage, Canvas, NW
import re
import os
from PIL import Image, ImageTk

from src._Variables import icono_v, Equipo

# Lista de ciudades y sus prefijos
ciudades = {
    "MED": "MEDELLIN",
    "CAL": "CALI",
    "BAR": "BARRANQUILLA",
    "BOG": "BOGOTA",
    "BUC": "BUCARAMANGA"
}

def extraer_detalles(nombre_completo):
    """ Extrae la ciudad, modelo, tipo y la IP del nombre del dispositivo """
    match = re.search(r"^([A-Z]+)_(\w+)_([A-Z])\s*\(([\d\.]+)\)$", nombre_completo)
    if match:
        prefijo_ciudad, modelo, tipo, ip = match.groups()
        ciudad = ciudades.get(prefijo_ciudad, "Desconocido")
        tipo_equipo = {"R": "Router", "S": "Switch", "A": "Access Point"}.get(tipo, "Desconocido")
        return ciudad, modelo, tipo_equipo, ip
    return "Desconocido", "Desconocido", "Desconocido", "IP no disponible"

def centrar_ventana(ventana, parent):
    """ Centra la ventana emergente en la aplicación principal """
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    x = parent.winfo_x() + (parent.winfo_width() - ancho) // 2
    y = parent.winfo_y() + (parent.winfo_height() - alto) // 2
    ventana.geometry(f"+{x}+{y}")

def ver_detalles(tree, parent, icono_path=None):
    """ Muestra una ventana emergente con los detalles del dispositivo seleccionado """
    item = tree.selection()
    if not item:
        messagebox.showwarning("Advertencia", "Seleccione un dispositivo primero")
        return
    
    nombre_completo = tree.item(item[0], "text")
    ciudad, modelo, tipo_equipo, ip = extraer_detalles(nombre_completo)

    # Crear una ventana emergente
    ventana = tk.Toplevel(parent)
    ventana.title("Device Details")
    ventana.geometry("350x200")
    ventana.transient(parent)
    ventana.grab_set()

    # Agregar icono si existe
    if icono_path and os.path.exists(icono_path):
        try:
            ventana.wm_iconbitmap(icono_path)
        except Exception as e:
            print(f"Error al cargar el icono: {e}")

    # Mostrar detalles
    tk.Label(ventana, text=f"{nombre_completo}", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(ventana, text=f"Ciudad: {ciudad}", font=("Arial", 10)).pack(pady=2)
    tk.Label(ventana, text=f"Modelo: {modelo}", font=("Arial", 10)).pack(pady=2)
    tk.Label(ventana, text=f"Tipo: {tipo_equipo}", font=("Arial", 10)).pack(pady=2)
    tk.Label(ventana, text=f"IP: {ip}", font=("Arial", 10)).pack(pady=5)

    tk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)

    # Centrar la ventana
    ventana.update_idletasks()
    centrar_ventana(ventana, parent)

# Función para agregar el dispositivo
def Add_device(tree, frame_center, size=(50, 50), bg_color=(240, 240, 240)):
    """ Muestra la imagen del equipo en frame_center sin eliminar las anteriores y sin transparencia """
    item = tree.selection()
    if not item:
        return  # No hace nada si no hay selección
    
    nombre_completo = tree.item(item[0], "text")  # Obtener nombre del equipo

    # Determinar la imagen para todos los equipos (sin distinción entre tipo de equipo)
    img_path = Equipo  # Imagen común para todos los equipos

    # Cargar la imagen y redimensionar
    img_pil = Image.open(img_path)  # Solo abrir la imagen
    img_pil = img_pil.resize(size, Image.Resampling.LANCZOS)  # Redimensionar

    img_tk = ImageTk.PhotoImage(img_pil)

    # Crear y mostrar la imagen en frame_center
    label_imagen = tk.Label(frame_center, image=img_tk, bg=f"#{bg_color[0]:02x}{bg_color[1]:02x}{bg_color[2]:02x}")
    label_imagen.image = img_tk  # Evita que el recolector de basura elimine la imagen
    label_imagen.place(relx=0.5, rely=0.5, anchor="center")  # Posiciona en el centro

    # Mantener referencia de los widgets agregados en un diccionario
    if not hasattr(frame_center, "devices"):
        frame_center.devices = {}
    
    frame_center.devices[label_imagen] = {'x': 0.5, 'y': 0.5}  # Guardar la referencia al label con su posición

    # Funcionalidad para mover la imagen
    def on_drag_start(event):
        """ Cuando se inicia el arrastre de la imagen """
        # Guardamos la posición inicial del mouse con respecto al label
        label_imagen.drag_data = {'x': event.x, 'y': event.y,
                                  'label_x': label_imagen.winfo_x(), 'label_y': label_imagen.winfo_y()}

    def on_drag_motion(event):
        """ Mueve la imagen mientras se arrastra """
        delta_x = event.x - label_imagen.drag_data['x']
        delta_y = event.y - label_imagen.drag_data['y']
        
        # Calculamos las nuevas coordenadas del Label
        new_x = label_imagen.drag_data['label_x'] + delta_x
        new_y = label_imagen.drag_data['label_y'] + delta_y
        
        # Movemos la imagen en la interfaz (sin crear un duplicado)
        label_imagen.place_configure(x=new_x, y=new_y)

        # Actualiza la referencia de la imagen para evitar que se pierda durante el arrastre
        label_imagen.image = img_tk  # Mantener la referencia a la imagen

        # Actualizamos la posición en el diccionario de dispositivos
        frame_center.devices[label_imagen] = {'x': new_x, 'y': new_y}

    def on_drag_end(event):
        """ Finaliza el arrastre de la imagen """
        label_imagen.drag_data = None

    # Bind de los eventos de arrastre
    label_imagen.bind("<ButtonPress-1>", on_drag_start)  # Evento cuando empieza el arrastre
    label_imagen.bind("<B1-Motion>", on_drag_motion)    # Evento mientras se mueve
    label_imagen.bind("<ButtonRelease-1>", on_drag_end)  # Evento cuando se suelta



