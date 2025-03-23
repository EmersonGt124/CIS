import os

# Listas de carpetas y archivos a excluir
EXCLUIR_CARPETAS = {"venv", "__pycache__", ".git", ".idea", "docs", "dist"}
EXCLUIR_ARCHIVOS = {"estructura.txt", "estructura.py"}

def listar_proyecto(ruta, archivo_salida, prefijo="- "):
    with open(archivo_salida, "w", encoding="utf-8") as f:
        for root, dirs, files in os.walk(ruta):
            # Filtrar carpetas a excluir
            dirs[:] = [d for d in dirs if d not in EXCLUIR_CARPETAS]

            nivel = root.replace(ruta, "").count(os.sep)
            indentacion = "  " * nivel
            linea = f"{indentacion}{prefijo}{os.path.basename(root)}/\n"
            f.write(linea)

            # Filtrar archivos antes de escribirlos
            for archivo in files:
                if archivo not in EXCLUIR_ARCHIVOS:
                    f.write(f"{indentacion}  - {archivo}\n")

ruta_proyecto = os.path.dirname(os.path.abspath(__file__))
archivo_salida = "estructura.txt"

listar_proyecto(ruta_proyecto, archivo_salida)
print(f"Estructura guardada en {archivo_salida}")
