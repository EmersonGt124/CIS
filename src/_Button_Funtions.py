import json
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tkinter import simpledialog, messagebox

from src._Variables import (
    save_settings,
    current_background_index, backgrounds,
    center_frame
    )


def load_settings():
    """Carga las configuraciones desde un archivo JSON o usa valores por defecto si no existe."""
    if os.path.exists(save_settings):  # Verifica si el archivo existe
        try:
            with open(save_settings, "r") as f:
                settings = json.load(f)
                current_background_index = settings.get("current_background_index", 0)

                # Asegurar que el índice es válido antes de aplicarlo
                if 0 <= current_background_index < len(backgrounds):
                    background = backgrounds[current_background_index]
                    #print(f"Fondo cargado correctamente: {_Variables.background}")
                else:
                    #print("Índice de fondo fuera de rango, usando fondo por defecto.")
                    current_background_index = 0
                    background = backgrounds[0]

        except json.JSONDecodeError:
            #print("Error en el archivo de configuración, restaurando valores por defecto.")
            save_settings()  # Si el archivo está corrupto, se sobrescribe con valores por defecto.
    else:
        #print("No se encontró el archivo de configuración, creando uno nuevo.")
        save_settings()  # Si no existe, se crea con valores por defecto.

def save_settings():
    """Guarda las configuraciones en un archivo JSON."""
    settings = {
        "current_background_index": current_background_index
    }
    with open(save_settings, "w") as f:
        json.dump(settings, f, indent=4)

#TOP BAR OPTIONS BUTTON

def add_device():
    print("Seleccionado: Add Device")

def themes():
    print("Seleccionado: Themes")

def toggle_background(): #Cambiar de fondo
    current_background_index = (current_background_index + 1) % len(backgrounds)

    new_background = backgrounds[current_background_index]

    if hasattr(center_frame) and center_frame:
        center_frame.set_background(new_background)  
        center_frame.update_idletasks()
        save_settings()
