#LIBRERIAS NECESARIAS
import tkinter as tk
from tkinter import ttk
from tkinter import Label, PhotoImage
from PIL import Image, ImageTk
import time
import random
import psycopg2
import os
import subprocess

#FUNCIONES Y VARIABLES INTERNAS
from src._Variables	import dbname, user, host, port
from src._Alerts import alerta_ok, alerta_error
from src._Control_interface import screen_control
from src._Button_Funtions import save_settings, load_settings

Centro_p = None

#CONEXION A LA BASE DE DATOS
def verificar_conectividad():
	"""Verifica conexión a Internet y a la BD local"""
	try:
		# Verificar Internet
		internet = subprocess.run(["ping", "-n", "1", "google.com"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		if internet.returncode != 0:
			_Alerts.alerta_ok("Error", "No hay conexión a Internet")
			al_cerrar_ventana()
			return False
		
		# Verificar conexión a localhost (127.0.0.1)
		localhost = subprocess.run(["ping", "-n", "1", "127.0.0.1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		if localhost.returncode != 0:
			_Alerts.alerta_ok("Error", "No hay conexión a la base de datos local")
			al_cerrar_ventana()
			return False

		return True
	except Exception as e:
		_Alerts.alerta_ok("Error", f"Error verificando conectividad: {e}")
		al_cerrar_ventana()
		return False
	
def conectar_bd(intentos=3):
	"""Conecta a PostgreSQL con usuario inicial (app_user)"""
	while intentos > 0:
		try:
			conn = psycopg2.connect(
				dbname=_Variables.dbname,
				user=_Variables.user,
				password="app_user123",
				host=_Variables.host,
				port=_Variables.port,
				client_encoding="UTF8"
			)
			return conn  # Conexión exitosa
		except psycopg2.Error as e:
			intentos -= 1
			n = _Alerts.alerta_error("Error", "No se pudo conectar a la BD", f"{e}")
			if n == 4:  # Opción "Reintentar"
				continue  # Intentar de nuevo
			elif n == 5:  # Opción "Omitir"
				al_cerrar_ventana()
			elif n == 3 or intentos == 0:  # Opción "Anular" o sin intentos restantes
				_Alerts.alerta_ok(f"Error", "Error", "Se agotaron los intentos de conexión.")
				al_cerrar_ventana()
				return None
	
def login_usuario(conn, username, password):
	"""Autentica al usuario de la tabla usuarios"""
	cursor = conn.cursor()
	
	cursor.execute("""
		SELECT id, username, rol_id 
		FROM usuarios 
		WHERE username = %s 
		AND password_hash = crypt(%s, password_hash);
	""", (username, password))

	user = cursor.fetchone()
	cursor.close()
	
	return user

def consultar_dispositivos(conn):
	"""Consulta los dispositivos permitidos para el usuario autenticado"""
	cursor = conn.cursor()
	cursor.execute("SELECT id, nombre, ip FROM dispositivos_permitidos;")
	dispositivos = cursor.fetchall()
	cursor.close()
	return dispositivos

def generar_numero_aleatorio(n1, n2):
	return random.randint(n1, n2)

def al_cerrar_ventana():
	save_settings()
	_Variables.root.destroy()

def screen_holding():
	subprocess.run(["lib/runs/Screen_Holding.exe"])

def seleccionar_label(label, imagen_original, imagen_hover):
	def cambiar_imagen(event):
		if event.type == tk.EventType.Enter:
			label.config(image=imagen_hover)
		elif event.type == tk.EventType.Leave:
			label.config(image=imagen_original)

	label.bind("<Enter>", cambiar_imagen)
	label.bind("<Leave>", cambiar_imagen)

def search_boton(logo, hover, ancho, alto, x, y, color, parent):
	image_original = Image.open(logo).convert("RGBA")
	image_original = image_original.resize((ancho, alto), Image.LANCZOS)
	photo_original = ImageTk.PhotoImage(image_original)
	label_image = tk.Label(parent, image=photo_original, bg=color)
	label_image.place(x=x, y=y)
	imagen_hover = Image.open(hover)
	imagen_hover = imagen_hover.resize((ancho, alto), Image.LANCZOS)
	photo_hover = ImageTk.PhotoImage(imagen_hover)

	seleccionar_label(label_image, photo_original, photo_hover)

	return label_image

def logos(logo, ancho, alto, x, y, color, parent):
	image = Image.open(logo).convert("RGBA")
	image = image.resize((ancho, alto), Image.Resampling.LANCZOS)  # Cambio aquí

	fondo_transparente = Image.new("RGBA", image.size, (255, 255, 255, 0))
	image_con_fondo_transparente = Image.alpha_composite(fondo_transparente, image)

	photo = ImageTk.PhotoImage(image_con_fondo_transparente)

	label_image = tk.Label(parent, image=photo, bg=color)  # Se pasó `Centro_p` como `parent`
	label_image.image = photo
	label_image.place(x=x, y=y)

	return label_image

def loading():
	#loading
	_Variables.Up_panel0 = logos(_Variables.Load_0_1, 503, 180, -3, -3, _Variables.Default, _Variables.Centro_p)
	_Variables.logo0 = logos(_Variables.Logo, 110, 110, 80, 40, "#DEEBF7", _Variables.Centro_p)
	_Variables.Down_panel0 = logos(_Variables.Load_0_2, 300, 150, 200, 450, _Variables.Default, _Variables.Centro_p)
	_Variables.Texto_calidad0 = tk.Label(_Variables.Centro_p, text="Loading...", fg="black", bg="#DEEBF7", font=(_Variables.fuente, 10))
	_Variables.Texto_calidad0.place(x=340, y=570)

	tiempo = generar_numero_aleatorio(3, 6)
	_Variables.Centro_p.after(tiempo * 1000, conecting_ping)

def conecting_ping():
	#loading
	_Variables.Up_panel0.place_forget()
	_Variables.logo0.place_forget()
	_Variables.Down_panel0.place_forget()
	_Variables.Texto_calidad0.place_forget()
	#conecting_ping
	_Variables.Up_panel1 = logos(_Variables.Load_1_1, 503, 180, -3, -3, _Variables.Default, _Variables.Centro_p)
	_Variables.logo1 = logos(_Variables.Logo, 110, 110, 80, 40, "#BDD7EE", _Variables.Centro_p)
	_Variables.Down_panel1 = logos(_Variables.Load_1_2, 300, 150, 200, 450, _Variables.Default, _Variables.Centro_p)
	_Variables.Texto_calidad1 = tk.Label(_Variables.Centro_p, text="Conecting to server…", fg="black", bg="#BDD7EE", font=(_Variables.fuente, 10))
	_Variables.Texto_calidad1.place(x=340, y=570)
	
	if not verificar_conectividad():
		return
	
	conn = conectar_bd()
	if not conn:
		return

	tiempo = generar_numero_aleatorio(3, 6)
	_Variables.Centro_p.after(tiempo * 1000, done)

def done():
	#conecting_ping
	_Variables.Up_panel1.place_forget()
	_Variables.logo1.place_forget()
	_Variables.Down_panel1.place_forget()
	_Variables.Texto_calidad1.place_forget()
	#done
	_Variables.Up_panel2 = logos(_Variables.Load_2_1, 503, 180, -3, -3, _Variables.Default, _Variables.Centro_p)
	_Variables.logo2 = logos(_Variables.Logo, 110, 110, 80, 40, "#9DC3E6", _Variables.Centro_p)
	_Variables.Down_panel2 = logos(_Variables.Load_2_2, 300, 150, 200, 450, _Variables.Default, _Variables.Centro_p)
	_Variables.Texto_calidad2 = tk.Label(Centro_p, text="Done…", fg="black", bg="#9DC3E6", font=(_Variables.fuente, 10))
	_Variables.Texto_calidad2.place(x=340, y=570)
	
	tiempo = generar_numero_aleatorio(3, 6)
	_Variables.Centro_p.after(tiempo * 1000, login_funcion)

def limpiar_frame(frame):
    """Elimina todos los widgets dentro de un frame y lo destruye completamente"""
    for widget in frame.winfo_children():
        widget.destroy()
    frame.pack_forget()  # También ocultar en caso de que siga visible
    frame.destroy()  # Eliminar el frame completamente

def iniciar_sesion():
    """Función principal del login en la interfaz"""
    if not verificar_conectividad():
        return

    conn = conectar_bd()
    if not conn:
        return

    if not _Variables.Name_entry or not _Variables.Pass_entry:
        _Alerts.alerta_ok("Error", "Error", "Los campos de usuario y contraseña no están disponibles.")
        return

    username = _Variables.Name_entry.get().strip()
    password = _Variables.Pass_entry.get().strip()

    if not username or not password:
        _Alerts.alerta_ok("Advertencia", "Advertencia", "Por favor, ingrese usuario y contraseña.")
        return

    user = login_usuario(conn, username, password)

    if user:
        user_id, username, rol_id = user
        _Alerts.alerta_ok("Éxito", "Éxito", f"Inicio de sesión exitoso. {username}")

        # Guardar la conexión en _Variables para su uso posterior
        _Variables.db_connection = conn
        _Variables.current_user = username

        limpiar_frame(_Variables.Centro_p)

        # Llamar a la nueva pantalla
        load_settings()
        screen_control(conn, username)

    else:
        _Alerts.alerta_ok("Error", "Error", "Usuario o contraseña incorrectos.")
        conn.close()

def login_funcion():
	# Ocultar la pantalla anterior
	_Variables.Up_panel2.place_forget()
	_Variables.logo2.place_forget()
	_Variables.Down_panel2.place_forget()
	_Variables.Texto_calidad2.place_forget()

	# Configurar la pantalla de login
	_Variables.Up_panel3 = logos(_Variables.Load_3_1, 503, 180, -3, -3, _Variables.Default, _Variables.Centro_p)
	_Variables.logo3 = search_boton(_Variables.Letters, _Variables.Letters1, 170, 100, 60, 20, "#1F4E79", _Variables.Centro_p)
	_Variables.Down_panel3 = logos(_Variables.Load_3_2, 300, 150, 200, 450, _Variables.Default, _Variables.Centro_p)

	"""
	# Entry username
	_Variables.Texto_Username = tk.Label(Centro_p, text="User Name (Nombre)", fg="white", bg=_Variables.Default, font=(_Variables.fuente, 15))
	_Variables.Texto_Username.place(x=270, y=210)
	_Variables.Name_entry = tk.Entry(Centro_p, width=21, font=(_Variables.fuente, 25), bg="#1F4E79", fg="white")
	_Variables.Name_entry.place(x=100, y=240)

	# Entry password
	_Variables.Texto_Pass = tk.Label(Centro_p, text="Password (Contraseña)", fg="white", bg=_Variables.Default, font=(_Variables.fuente, 15))
	_Variables.Texto_Pass.place(x=270, y=300)
	_Variables.Pass_entry = tk.Entry(Centro_p, show="*", width=21, font=(_Variables.fuente, 25), bg="#1F4E79", fg="white")
	_Variables.Pass_entry.place(x=100, y=330)
	"""

	# Entry username con valor por defecto
	_Variables.Texto_Username = tk.Label(_Variables.Centro_p, text="User Name (Nombre)", fg="white", bg=_Variables.Default, font=(_Variables.fuente, 15))
	_Variables.Texto_Username.place(x=270, y=210)
	_Variables.Name_entry = tk.Entry(_Variables.Centro_p, width=21, font=(_Variables.fuente, 25), bg="#1F4E79", fg="white")
	_Variables.Name_entry.place(x=100, y=240)
	_Variables.Name_entry.insert(0, "egranda")  # Inserta el usuario por defecto

	# Entry password con valor por defecto
	_Variables.Texto_Pass = tk.Label(_Variables.Centro_p, text="Password (Contraseña)", fg="white", bg=_Variables.Default, font=(_Variables.fuente, 15))
	_Variables.Texto_Pass.place(x=270, y=300)
	_Variables.Pass_entry = tk.Entry(_Variables.Centro_p, show="*", width=21, font=(_Variables.fuente, 25), bg="#1F4E79", fg="white")
	_Variables.Pass_entry.place(x=100, y=330)
	_Variables.Pass_entry.insert(0, "egranda123")  # Inserta la contraseña por defecto

	# Help button
	_Variables.help_text = search_boton(_Variables.help_letter, _Variables.help_letter1, 110, 35, 15, 537, _Variables.Default, _Variables.Centro_p)

	#enter login
	_Variables.Name_entry.bind("<Return>", lambda e: iniciar_sesion())  # Enter en username
	_Variables.Pass_entry.bind("<Return>", lambda e: iniciar_sesion()) 

	# Login button
	_Variables.login_B = search_boton(_Variables.login, _Variables.login1, 110, 35, 370, 535, "#1F4E79", _Variables.Centro_p)
	_Variables.login_B.bind("<Button-1>", lambda e: iniciar_sesion())

def Login_Windows():
	_Variables.root.title(_Variables.titulo)
	_Variables.root.iconbitmap(_Variables.icono_v)
	_Variables.root.geometry(f"{500}x{600}")
	_Variables.root.resizable(0,0)

	_Variables.Centro_p = tk.Frame(_Variables.root, bg=_Variables.Default)
	_Variables.Centro_p.pack(side="top", fill="both", expand=True)

	loading()
	
	_Variables.root.protocol("WM_DELETE_WINDOW", al_cerrar_ventana)
	_Variables.root.mainloop()