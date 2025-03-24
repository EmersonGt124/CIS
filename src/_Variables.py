import tkinter as tk 
from tkinter import font
import getpass
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#Convert Indentation to Taps

##########################
	  #VENTANA
##########################
#Variables inicializador de ventana
root = tk.Tk() #inicializar tk ventana root

titulo = "CIS - LOGIN"
#icono_v = "lib/assets/Images/Logo/Logo.ico"
icono_v = os.path.abspath(os.path.join(os.path.dirname(__file__), "../lib/assets/Images/Logo/Logo.ico"))

##########################
	  #DATA
##########################
Usuario = getpass.getuser()

##########################
	#VENTANA FUENTES
##########################
# Registrar la fuente en tkinter
fuente_negrita = ("Calibri", 12, "bold")
fuente = ("Calibri", 12)
##########################
	#DOCUMENTOS
##########################

#loading images
Load_0_1 = "lib/assets/Images/Loading/0-1.png"
Load_0_2 = "lib/assets/Images/Loading/0-2.png"
Load_1_1 = "lib/assets/Images/Loading/1-1.png"
Load_1_2 = "lib/assets/Images/Loading/1-2.png"
Load_2_1 = "lib/assets/Images/Loading/2-1.png"
Load_2_2 = "lib/assets/Images/Loading/2-2.png"
Load_3_1 = "lib/assets/Images/Loading/3-1.png"
Load_3_2 = "lib/assets/Images/Loading/3-2.png"

#login images
login_entry = "lib/assets/Images/Login/entry.png"
login = "lib/assets/Images/Login/login.png"
login1 = "lib/assets/Images/Login/login1.png"

#logotipes images
Letters = "lib/assets/Images/Logo/Letters.png"
Letters1 = "lib/assets/Images/Logo/Letters1.png"
Logo = "lib/assets/Images/Logo/Logo.png"

#help images
help_letter = "lib/assets/Images/Login/Help.png"
help_letter1 = "lib/assets/Images/Login/Help1.png"

#Next imagen
next_imagen = "lib/assets/Images/Control/next_imagen.png"

# Variables para el nombre y la IP del dispositivo
dispositivo_nombre = ""
dispositivo_ip = ""

# Rutas de las imágenes de los equipos
Equipo_bad = "lib/assets/Images/control/switch_bad.png"
Equipo = "lib/assets/Images/control/switch_good.png"

# Ruta Data save_settings
setting = "lib/assets/config.json"

image_list = [
    "lib/assets/Images/Background/Map1.png",
    "lib/assets/Images/Background/Map2.png",
    "lib/assets/Images/Background/Map3.png",
    "lib/assets/Images/Background/Map4.png",
    "lib/assets/Images/Background/Map5.png",
    "lib/assets/Images/Background/Map6.png",
    "lib/assets/Images/Background/Map7.png"
]

##########################
	#VENTANA COLORES
##########################
Default = "#01244A" #background default
B_selecion = "#C7C7C9" #selection bottons effect color

C_fondo = "#01244A" #color fondo azul oscuro
C_toggles = "#1F4E79" #color app azul medio barras laterales
C_fondo_2 = "#1F4E79" #segundo color fondo laterales
C_texto_Azul = "#5597D3" # textos

C_texto_blanco = "#FFFFFF" #color barras blanco arrina y abajo
C_texto_negro = "#000000" #color texto negro


##########################
	#DIRECCIONES DB
##########################
dbname="isp_networks" #database nombre
user="app_user" #usuario login db
host="127.0.0.1" #IP SERVIDOR BASE DE DATOS.
port="5432" #PUERTO SERVIDOR BASE DE DATOS.

username = "" #CLIENTE CONSULTA
password = "" #CLIENTE CONSULTA

db_connection = "conn"
current_user = "username"

#Botones Top bar
btn_Home = None
btn_Options = None
btn_Help = None

#Widgets
Up_panel0 = None
logo0 = None
Down_panel0 = None
Texto_calidad0 = None
#conecting_ping:
Up_panel1 = None
logo1 = None
Down_panel1 = None
Texto_calidad1 = None
#done:
Up_panel2 = None
logo2 = None
Down_panel2 = None
Texto_calidad2 = None
#login:
Up_panel3 = None
logo3 = None
Down_panel3 = None
#entry username
Texto_Username = None
Name_entry = None
#entry password
Texto_Pass = None
Pass_entry = None
#help boton
help_text = None
login_B = None

#Frames
center_frame = None
Centro_p = None

left_frame = None
left_toggle_button = None
left_expanded = None
right_frame = None
right_toggle_button = None
right_expanded = None