import os
import shutil

# Ruta del icono
icono_v = os.path.abspath("F:/Documentos/GitHub/LOGIN/lib/assets/Images/Logo/Logo.ico")

# Verificar si el icono existe antes de compilar
if not os.path.exists(icono_v):
    print(f"Error: No se encontró el icono en {icono_v}")
    exit(1)

# Carpeta de destino para el ejecutable (modificar según necesidad)
output_dir = os.path.abspath("F:/Documentos/GitHub/LOGIN/lib/runs/")  # Cambia a donde quieras guardar el .exe

# Asegurar que la carpeta de salida exista
os.makedirs(output_dir, exist_ok=True)

# Comando para compilar con PyInstaller
comando = [
    "pyinstaller",
    "--onefile",
    "--noconsole",
    "--name", "Screen_Holding",
    "--icon", icono_v,  # Ruta absoluta del icono
    "--distpath", output_dir,  # Especifica el directorio de salida
    "_Screen_Holding.py"
]

print("Starting compilation...")
resultado = os.system(" ".join(comando))

if resultado == 0:
    print(f"Compilation successful. Executable saved in: {output_dir}")
else:
    print("Compilation failed.")
