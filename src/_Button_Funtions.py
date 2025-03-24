import tkinter as tk
from tkinter import messagebox, Label, PhotoImage, Canvas, NW
import re
import os
from PIL import Image, ImageTk

from src._Variables import icono_v, Equipo_switch, Equipo_router

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

def ver_detalles(tree, parent, icono_path=icono_v):
    """ Muestra una ventana emergente con los detalles del dispositivo seleccionado """
    item = tree.selection()
    if not item:
        messagebox.showwarning("Advertencia", "Seleccione un dispositivo primero")
        return
    
    item_id = item[0]  
    nombre_completo = tree.item(item_id, "text")  

    ciudad, modelo, tipo_equipo, ip = extraer_detalles(nombre_completo)

    # Crear una ventana emergente anclada al parent
    ventana = tk.Toplevel(parent)
    ventana.title("Device Details")
    ventana.geometry("350x200")
    ventana.transient(parent)  # Evita que quede detrás del frame principal
    ventana.grab_set()  # Bloquea interacción con la ventana principal hasta cerrarla

    # Agregar icono si se proporciona una ruta
    if icono_path and os.path.exists(icono_path):
        try:
            ventana.wm_iconbitmap(icono_path)  # SOLO PARA ARCHIVOS .ICO
        except Exception as e:
            print(f"Error al cargar el icono: {e}")

    # Mostrar detalles
    tk.Label(ventana, text=f"{nombre_completo}", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(ventana, text=f"Ciudad: {ciudad}", font=("Arial", 10)).pack(pady=2)
    tk.Label(ventana, text=f"Modelo: {modelo}", font=("Arial", 10)).pack(pady=2)
    tk.Label(ventana, text=f"Tipo: {tipo_equipo}", font=("Arial", 10)).pack(pady=2)
    tk.Label(ventana, text=f"IP: {ip}", font=("Arial", 10)).pack(pady=5)

    tk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)

    # Centrar la ventana en la aplicación
    ventana.update_idletasks()
    centrar_ventana(ventana, parent)

#DEVICES CENTER
def Add_device(tree, frame_center, size=(100, 100)):  
    """ Superpone la imagen del equipo en frame_center sin perder la transparencia 
        y permite redimensionarla al tamaño especificado. """
    
    item = tree.selection()
    if not item:
        return  # No hace nada si no hay selección
    
    nombre_completo = tree.item(item[0], "text")  # Obtener nombre del equipo

    # Determinar la imagen según el tipo de equipo
    if "_R" in nombre_completo:
        img_path = Equipo_router
    elif "_S" in nombre_completo:
        img_path = Equipo_switch
    else:
        return  # No muestra imagen si no es router ni switch

    # Cargar la imagen con PIL y mantener transparencia
    img_pil = Image.open(img_path).convert("RGBA")  

    # Redimensionar la imagen al tamaño deseado
    img_pil = img_pil.resize(size, Image.Resampling.LANCZOS)

    img_tk = ImageTk.PhotoImage(img_pil)

    # Crear un Canvas para manejar la imagen con transparencia
    canvas = Canvas(frame_center, width=size[0], height=size[1], highlightthickness=0, bg=frame_center.cget("bg"))
    canvas.create_image(0, 0, image=img_tk, anchor=NW)

    # Eliminar imágenes previas y agregar la nueva
    for widget in frame_center.winfo_children():
        widget.destroy()

    canvas.image = img_tk  # Evita que la imagen sea eliminada por el recolector de basura
    canvas.place(relx=0.5, rely=0.5, anchor="center")  # Centrar la imagen en el frame
    canvas.lift()  # Traer la imagen al frente
