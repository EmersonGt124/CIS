import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Cargar la imagen del mapa
image_path = "Map6.png"  # Reemplaza con la ruta de tu imagen
img = mpimg.imread(image_path)

# Diccionario para almacenar las etiquetas
region_tags = {}

def get_label_details(root):
    """Muestra una ventana emergente centrada sobre la aplicación para ingresar el nombre de la región."""
    def submit():
        """Captura el nombre ingresado y cierra la ventana."""
        label_name = entry_name.get().strip()
        if not label_name:
            messagebox.showwarning("Nombre vacío", "Debe ingresar un nombre.", parent=window)
            return

        user_input["name"] = label_name
        window.quit()  # Cierra la ventana sin terminar el script
        window.destroy()

    # Crear ventana emergente
    window = tk.Toplevel(root)
    window.title("Agregar Región")
    window.geometry("300x120")
    window.resizable(False, False)
    window.grab_set()  # Bloquea la interacción con la ventana principal
    window.attributes('-topmost', True)  # Mantiene la ventana en primer plano

    # Centrar ventana respecto a la aplicación
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    
    win_x = root_x + (root_width // 2) - (300 // 2)  # Centrar en X
    win_y = root_y + (root_height // 2) - (120 // 2)  # Centrar en Y
    window.geometry(f"+{win_x}+{win_y}")

    # Elementos de la ventana
    tk.Label(window, text="Ingrese el nombre de la región:").pack(pady=5)

    entry_name = tk.Entry(window)
    entry_name.pack(pady=5)

    tk.Button(window, text="Aceptar", command=submit).pack(pady=10)

    window.mainloop()
    return user_input if "name" in user_input else None  # Retorna datos si se ingresaron correctamente

def is_visible(event):
    """Verifica si el clic se hizo en un área NO transparente (visible del mapa)."""
    if img.shape[-1] == 4:  # Verifica si la imagen tiene canal alfa
        x, y = int(event.xdata), int(event.ydata)
        if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:  # Verifica que esté dentro de la imagen
            return img[y, x, 3] > 0  # Solo permite clics en píxeles con alfa mayor a 0 (no transparentes)
    return True  # Si no tiene canal alfa, se considera completamente visible

def add_region(event):
    """Función para agregar una región en la posición del clic solo en áreas visibles."""
    if event.xdata is None or event.ydata is None:
        return  # Evita clics fuera de la imagen

    if not is_visible(event):
        return  # No abrir la ventana si el área es transparente

    details = get_label_details(root)
    if not details:
        return  # Si se cierra la ventana sin ingresar datos, salir

    label_name = details["name"]

    # Verificar si el nombre ya existe
    if label_name in region_tags:
        messagebox.showwarning("Duplicado", f"La región '{label_name}' ya existe.")
        return

    region_tags[label_name] = (event.xdata, event.ydata)
    print(f"Etiqueta añadida: Región - {label_name} -> {event.xdata}, {event.ydata}")

    # Dibujar la etiqueta en el mapa
    plt.scatter(event.xdata, event.ydata, c='red', marker='x')
    plt.text(event.xdata, event.ydata, label_name, fontsize=12, color='white', 
             bbox=dict(facecolor='black', alpha=0.5))
    plt.draw()

# Inicializar variable para almacenar datos del usuario
user_input = {}

# Crear ventana de Tkinter
root = tk.Tk()
root.withdraw()  # Oculta la ventana principal de Tkinter

# Mostrar la imagen con matplotlib
fig, ax = plt.subplots()
ax.imshow(img)

# Conectar el evento de clic para agregar etiquetas solo en áreas visibles
fig.canvas.mpl_connect('button_press_event', add_region)

plt.show()
