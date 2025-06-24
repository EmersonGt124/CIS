import tkinter as tk
from tkinter import messagebox, Label, PhotoImage, Canvas, NW
import re
import os
from PIL import Image, ImageTk
import json

from src._Variables import (
    icono_v, Equipo, setting,
    C_texto_blanco
    )
from src._Alerts import alerta_ok

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

#Guardar datos en JSON
def save_setting_to_json(key, value):
    """Guarda o actualiza una configuración en el archivo JSON."""
    try:
        # Cargar datos existentes si el archivo existe
        if os.path.exists(setting):
            with open(setting, "r", encoding="utf-8") as file:
                data = json.load(file)
        else:
            data = {}

        # Asegurar que 'settings' existe
        if "settings" not in data:
            data["settings"] = {}

        # Actualizar o agregar el valor
        data["settings"][key] = value

        # Guardar de nuevo el archivo JSON
        with open(setting, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    except Exception as e:
        print(f"Error al guardar la configuración: {e}")

def load_settings_from_json():
    """Carga las configuraciones guardadas desde el archivo JSON."""
    if os.path.exists(setting):
        try:
            with open(setting, "r", encoding="utf-8") as file:
                settings = json.load(file).get("settings", {})
                return settings  # Retorna el diccionario con la configuración
        except Exception as e:
            print(f"Error al cargar la configuración: {e}")
    return {}  # Retorna un diccionario vacío si no hay configuración

# Función para agregar el dispositivo

def Add_device(tree, frame_center, size=(50, 50), bg_color=(240, 240, 240)):
    item = tree.selection()
    if not item or len(item) == 0:
        alerta_ok("Alerta", "Selección requerida", "Por favor, seleccione un dispositivo antes de agregarlo.")
        return
    
    nombre_completo = tree.item(item[0], "text")  # Obtener nombre del equipo
    img_path = Equipo  # Imagen común para todos los equipos
    text_color=C_texto_blanco

    img_pil = Image.open(img_path).resize(size, Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_pil)
    
    if not hasattr(frame_center, "devices"):
        frame_center.devices = []
    
    def find_free_position():
        padding = 10  # Espacio extra entre dispositivos
        x, y = 100, 100  # Posición inicial por defecto
        
        while any(abs(x - device['label'].winfo_x()) < size[0] + padding and
                  abs(y - device['label'].winfo_y()) < size[1] + padding 
                  for device in frame_center.devices):
            x += size[0] + padding
            if x + size[0] > frame_center.winfo_width():  # Si se sale del marco, bajar una fila
                x = 100
                y += size[1] + padding
        
        return x, y
    
    pos_x, pos_y = find_free_position()
    
    label_imagen = tk.Label(frame_center, image=img_tk, bg=f"#{bg_color[0]:02x}{bg_color[1]:02x}{bg_color[2]:02x}")
    label_imagen.image = img_tk  
    label_imagen.place(x=pos_x, y=pos_y)
    
    label_nombre = tk.Label(frame_center, text=nombre_completo, fg=text_color, bg=frame_center.cget("bg"), font=("Arial", 10, "bold"))
    label_nombre.place(x=pos_x + size[0] // 2, y=pos_y - 15, anchor="center")
    
    frame_center.devices.append({'label': label_imagen, 'name': label_nombre})
    
    def check_collision(new_x, new_y):
        for device in frame_center.devices:
            label = device['label']
            if label == label_imagen:
                continue
            
            dx = abs(new_x - label.winfo_x())
            dy = abs(new_y - label.winfo_y())
            if dx < size[0] and dy < size[1]:
                return True
        return False
    
    def on_drag_start(event):
        label_imagen.drag_data = {'x': event.x_root, 'y': event.y_root, 'orig_x': label_imagen.winfo_x(), 'orig_y': label_imagen.winfo_y()}
    
    def on_drag_motion(event):
        delta_x = event.x_root - label_imagen.drag_data['x']
        delta_y = event.y_root - label_imagen.drag_data['y']
        
        new_x = label_imagen.drag_data['orig_x'] + delta_x
        new_y = label_imagen.drag_data['orig_y'] + delta_y
        
        # Limitar el movimiento dentro del frame_center
        max_x = frame_center.winfo_width() - size[0]
        max_y = frame_center.winfo_height() - size[1]
        new_x = max(0, min(new_x, max_x))
        new_y = max(0, min(new_y, max_y))
        
        if not check_collision(new_x, new_y):
            label_imagen.place(x=new_x, y=new_y)
            label_nombre.place(x=new_x + size[0] // 2, y=new_y - 15, anchor="center")
    
    label_imagen.bind("<ButtonPress-1>", on_drag_start)
    label_imagen.bind("<B1-Motion>", on_drag_motion)
