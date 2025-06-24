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

import bcrypt
import time


#FUNCIONES Y VARIABLES INTERNAS
from src._Variables	import (
	dbname, user, host, port, Name_entry, Pass_entry,
	Up_panel0, Up_panel2, logo2, Down_panel2,
	Texto_calidad2, Letters1, Letters, Up_panel3,
	Logo, logo3, Down_panel3, Texto_Pass, fuente,
	help_letter, help_letter1, help_text, login_B,
	login, login1, titulo, icono_v, Default,
	root,
	Load_0_1, Load_0_2, Load_1_1, Load_1_2, Load_2_1, Load_2_2, Load_3_1, Load_3_2
	)
from src._Alerts import alerta_ok, alerta_error
from src._Control_interface import screen_control

Centro_p = None

#CONEXION A LA BASE DE DATOS
def verificar_conectividad():
	"""Verifica conexión a Internet y a la BD local"""
	try:
		# Verificar Internet
		internet = subprocess.run(["ping", "-n", "1", "google.com"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		if internet.returncode != 0:
			alerta_ok("Error", "No hay conexión a Internet")
			al_cerrar_ventana()
			return False
		
		# Verificar conexión a localhost (127.0.0.1)
		localhost = subprocess.run(["ping", "-n", "1", "127.0.0.1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		if localhost.returncode != 0:
			alerta_ok("Error", "No hay conexión a la base de datos local")
			al_cerrar_ventana()
			return False

		return True
	except Exception as e:
		alerta_ok("Error", f"Error verificando conectividad: {e}")
		al_cerrar_ventana()
		return False
	
def conectar_bd(intentos=3):
	"""Conecta a PostgreSQL con usuario inicial (app_user)"""
	while intentos > 0:
		try:
			conn = psycopg2.connect(
				dbname=dbname,
				user=user,
				password="app_user123",
				host=host,
				port=port,
				client_encoding="UTF8"
			)
			return conn  # Conexión exitosa
		except psycopg2.Error as e:
			intentos -= 1
			n = alerta_error("Error", "No se pudo conectar a la BD", f"{e}")
			if n == 4:  # Opción "Reintentar"
				continue  # Intentar de nuevo
			elif n == 5:  # Opción "Omitir"
				al_cerrar_ventana()
			elif n == 3 or intentos == 0:  # Opción "Anular" o sin intentos restantes
				alerta_ok(f"Error", "Error", "Se agotaron los intentos de conexión.")
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
	#save_settings()
	root.destroy()

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

def conecting_ping():
	#conecting_ping
	Up_panel1 = logos(Load_1_1, 503, 180, -3, -3, Default, Centro_p)
	logo1 = logos(Logo, 110, 110, 80, 40, "#BDD7EE", Centro_p)
	Down_panel1 = logos(Load_1_2, 300, 150, 200, 450, Default, Centro_p)
	Texto_calidad1 = tk.Label(Centro_p, text="Conecting to server…", fg="black", bg="#BDD7EE", font=(fuente, 10))
	Texto_calidad1.place(x=340, y=570)
	
	if not verificar_conectividad():
		return
	
	conn = conectar_bd()
	if not conn:
		return

	tiempo = generar_numero_aleatorio(3, 6)
	Centro_p.after(tiempo * 1000, done)

def done():
	#done
	Up_panel2 = logos(Load_2_1, 503, 180, -3, -3, Default, Centro_p)
	logo2 = logos(Logo, 110, 110, 80, 40, "#9DC3E6", Centro_p)
	Down_panel2 = logos(Load_2_2, 300, 150, 200, 450, Default, Centro_p)
	Texto_calidad2 = tk.Label(Centro_p, text="Done…", fg="black", bg="#9DC3E6", font=(fuente, 10))
	Texto_calidad2.place(x=340, y=570)
	
	tiempo = generar_numero_aleatorio(3, 6)
	Centro_p.after(tiempo * 1000, login_funcion)

def limpiar_frame(frame):
    """Elimina todos los widgets dentro de un frame y lo destruye completamente"""
    for widget in frame.winfo_children():
        widget.destroy()
    frame.pack_forget()  # También ocultar en caso de que siga visible
    frame.destroy()  # Eliminar el frame completamente

login_attempts = {}

def iniciar_sesion(Name_entry, Pass_entry):
    """Función principal del login en la interfaz con medidas de seguridad mejoradas."""
    if not verificar_conectividad():
        return

    conn = conectar_bd()
    if not conn:
        return

    if not Name_entry or not Pass_entry:
        alerta_ok("Error", "Error", "Los campos de usuario y contraseña no están disponibles.")
        return

    username = Name_entry.get().strip()
    password = Pass_entry.get().strip()

    if not username or not password:
        alerta_ok("Advertencia", "Advertencia", "Por favor, ingrese usuario y contraseña.")
        return

    # Bloqueo temporal tras demasiados intentos fallidos
    if username in login_attempts and login_attempts[username]['attempts'] >= 3:
        if time.time() - login_attempts[username]['timestamp'] < 60:  # 60 segundos de bloqueo
            alerta_ok("Error", "Error", "Demasiados intentos fallidos. Intente de nuevo más tarde.")
            return
        else:
            login_attempts[username] = {'attempts': 0, 'timestamp': time.time()}  # Reset de intentos

    user = login_usuario(conn, username)

    if user:
        user_id, username_db, hashed_password, rol_id = user

        if bcrypt.checkpw(password.encode(), hashed_password.encode()):
            alerta_ok("Éxito", "Éxito", f"Inicio de sesión exitoso. {username}")

            # Reset de intentos fallidos tras éxito
            if username in login_attempts:
                del login_attempts[username]

            # Guardar la conexión en variables globales
            db_connection = conn
            current_user = username_db

            limpiar_frame(Centro_p)
            screen_control(conn, username_db)
            return

    # Manejo de fallos en autenticación
    alerta_ok("Error", "Error", "Usuario o contraseña incorrectos.")
    login_attempts.setdefault(username, {'attempts': 0, 'timestamp': time.time()})
    login_attempts[username]['attempts'] += 1
    login_attempts[username]['timestamp'] = time.time()
    conn.close()

def login_usuario(conn, username):
    """Consulta segura a la base de datos para recuperar usuario y contraseña hasheada."""
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash, rol_id FROM usuarios WHERE username = %s", (username,))
    return cur.fetchone()

def login_funcion():

	# Configurar la pantalla de login
	Up_panel3 = logos(Load_3_1, 503, 180, -3, -3, Default, Centro_p)
	logo3 = search_boton(Letters, Letters1, 170, 100, 60, 20, "#1F4E79", Centro_p)
	Down_panel3 = logos(Load_3_2, 300, 150, 200, 450, Default, Centro_p)

	"""
	# Entry username
	Texto_Username = tk.Label(Centro_p, text="User Name (Nombre)", fg="white", bg=Default, font=(fuente, 15))
	Texto_Username.place(x=270, y=210)
	Name_entry = tk.Entry(Centro_p, width=21, font=(fuente, 25), bg="#1F4E79", fg="white")
	Name_entry.place(x=100, y=240)

	# Entry password
	Texto_Pass = tk.Label(Centro_p, text="Password (Contraseña)", fg="white", bg=Default, font=(fuente, 15))
	Texto_Pass.place(x=270, y=300)
	Pass_entry = tk.Entry(Centro_p, show="*", width=21, font=(fuente, 25), bg="#1F4E79", fg="white")
	Pass_entry.place(x=100, y=330)
	"""

	# Entry username con valor por defecto
	Texto_Username = tk.Label(Centro_p, text="User Name (Nombre)", fg="white", bg=Default, font=(fuente, 15))
	Texto_Username.place(x=270, y=210)
	Name_entry = tk.Entry(Centro_p, width=21, font=(fuente, 25), bg="#1F4E79", fg="white")
	Name_entry.place(x=100, y=240)
	Name_entry.insert(0, "egranda")  # Inserta el usuario por defecto

	# Entry password con valor por defecto
	Texto_Pass = tk.Label(Centro_p, text="Password (Contraseña)", fg="white", bg=Default, font=(fuente, 15))
	Texto_Pass.place(x=270, y=300)
	Pass_entry = tk.Entry(Centro_p, show="*", width=21, font=(fuente, 25), bg="#1F4E79", fg="white")
	Pass_entry.place(x=100, y=330)
	Pass_entry.insert(0, "egranda123")  # Inserta la contraseña por defecto

	# Help button
	help_text = search_boton(help_letter, help_letter1, 110, 35, 15, 537, Default, Centro_p)

	#enter login
	Name_entry.bind("<Return>", lambda e: iniciar_sesion(Name_entry, Pass_entry))  # Enter en username
	Pass_entry.bind("<Return>", lambda e: iniciar_sesion(Name_entry, Pass_entry))

	# Login button
	login_B = search_boton(login, login1, 110, 35, 370, 535, "#1F4E79", Centro_p)
	login_B.bind("<Button-1>", lambda e: iniciar_sesion(Name_entry, Pass_entry))

def Login_Windows():
	global Centro_p

	root.title(titulo)
	root.iconbitmap(icono_v)
	root.geometry(f"{500}x{600}")
	root.resizable(0,0)

	Centro_p = tk.Frame(root, bg=Default)
	Centro_p.pack(side="top", fill="both", expand=True)

	loading()
	
	root.protocol("WM_DELETE_WINDOW", al_cerrar_ventana)
	root.mainloop()

def loading():
	global Centro_p
	#loading
	Up_panel0 = logos(Load_0_1, 503, 180, -3, -3, Default, Centro_p)
	logo0 = logos(Logo, 110, 110, 80, 40, "#DEEBF7", Centro_p)
	Down_panel0 = logos(Load_0_2, 300, 150, 200, 450, Default, Centro_p)
	Texto_calidad0 = tk.Label(Centro_p, text="Loading...", fg="black", bg="#DEEBF7", font=(fuente, 10))
	Texto_calidad0.place(x=340, y=570)

	tiempo = generar_numero_aleatorio(3, 6)
	Centro_p.after(tiempo * 1000, conecting_ping)
