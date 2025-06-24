# LIBRERÍAS NECESARIAS
import tkinter as tk
from tkinter import ttk
import psycopg2
from PIL import Image, ImageTk
import os

# FUNCIONES Y VARIABLES INTERNAS
from src._Variables import (
    left_expanded, left_frame, left_toggle_button, 
    right_expanded, right_frame, right_toggle_button,
    C_fondo, C_texto_blanco, C_fondo_2, C_texto_Azul, C_fondo_2,
    fuente, icono_v, image_list, B_selecion,
    db_connection,
    btn_Home, btn_Options, btn_Help,
    root, center_frame
    )

from src._Button_Funtions import ver_detalles, Add_device, save_setting_to_json, load_settings_from_json

active_menus = []

def toggle_left_bar():
    global left_expanded, left_frame
    """Expande o colapsa el frame izquierdo."""
    
    if left_frame is None:  # Evitar errores si no está inicializado
        print("Error: left_frame no está inicializado")
        return

    if left_expanded:
        left_frame.config(width=10)
        left_toggle_button.config(text="▶")
    else:
        left_frame.config(width=300)
        left_toggle_button.config(text="◀")

    left_expanded = not left_expanded
    left_frame.update_idletasks()

def toggle_right_bar():
    global right_expanded, right_frame, right_toggle_button
    
    if right_frame is None or right_toggle_button is None:
        print("Error: right_frame o right_toggle_button no están inicializados")
        return

    """Expande o colapsa el frame derecho."""
    if right_expanded:
        right_frame.config(width=10)  # Reducir a solo el botón visible
        right_toggle_button.config(text="◀")  # Flecha apuntando a la izquierda
    else:
        right_frame.config(width=300)  # Expandir nuevamente
        right_toggle_button.config(text="▶")  # Flecha apuntando a la derecha

    right_expanded = not right_expanded  # Alternar estado
    right_frame.update_idletasks()  # Forzar actualización de la GUII

def on_enter(e):
    e.widget.config(fg=C_texto_blanco, bg=C_fondo_2)  

def on_leave(e):
    e.widget.config(fg=C_texto_blanco, bg=C_fondo) 

def show_submenu(event, options, parent_menu=None, offset_x=0, offset_y=0):
    """Muestra un menú contextual en la posición deseada"""
    global active_menus

    # Cerrar cualquier submenú abierto en el mismo nivel
    if parent_menu:
        for m in active_menus[:]:
            if m != parent_menu and m.winfo_exists():
                m.destroy()
                active_menus.remove(m)

    # Crear un nuevo menú emergente
    menu = tk.Toplevel()
    menu.overrideredirect(True)  # Quita la barra de título
    menu.configure(bg=C_fondo)

    # Guardar referencia del menú activo
    active_menus.append(menu)

    # Obtener posición base del menú
    if parent_menu:
        parent_menu.update_idletasks()  # Asegurar que se actualiza la geometría
        x = parent_menu.winfo_rootx() + parent_menu.winfo_width()  # Posiciona a la derecha
        y = parent_menu.winfo_rooty() + offset_y  # Mantiene la alineación vertical
    else:
        button = event.widget
        x = button.winfo_rootx()
        y = button.winfo_rooty() + button.winfo_height()

    menu.geometry(f"+{x}+{y}")

    # Función vacía en caso de que una opción no tenga una función asignada
    def noop():
        pass  # No hace nada

    # Crear botones dentro del submenú
    for text, command in options:
        btn = tk.Button(menu, text=text, bg=C_fondo, fg=C_texto_blanco,
                        font=fuente, bd=0, padx=10, pady=5, relief="flat")
        btn.pack(fill="x", padx=5, pady=2)

        # Aplicar efectos de hover
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        # Si la opción tiene un submenú, abrirlo a la derecha cuando se haga clic
        if isinstance(command, list):  # Submenú
            btn.config(command=lambda cmd=command: show_submenu(
                event, cmd, menu,  
                offset_x=btn.winfo_width(),  
                offset_y=btn.winfo_y()
            ))
        else:
            # Verificar que `command` no sea `None` antes de ejecutarlo
            btn.config(command=lambda cmd=command: [cmd(), close_menus()] if cmd else close_menus())

    # Asegurar que el menú se cierre si se hace clic fuera
    def close_on_click(event):
        if event is None:
            return  # Evita errores si el evento es None

        try:
            if event.x_root is None or event.y_root is None:
                return  # Evita errores si las coordenadas no existen

            if not menu.winfo_containing(event.x_root, event.y_root):
                close_menus()
        except:
            pass  # Evita errores si Tkinter ya cerró la ventana

    menu.bind("<FocusOut>", close_on_click)
    menu.focus_force()

def close_menus():
    """Cierra todos los menús activos"""
    global active_menus
    for menu in active_menus:
        if menu.winfo_exists():
            menu.destroy()
    active_menus = []

class ZoomableCanvas(tk.Frame):
    def __init__(self, parent, image_list):
        super().__init__(parent, bg=C_fondo)

        # Crear el canvas sin bordes visibles
        self.canvas = tk.Canvas(self, bg=C_fondo, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Configuración predeterminada de zoom
        self.zoom_factor = 1.0
        self.zoom_step = 0.2
        self.max_zoom = 3.0
        self.min_zoom = 1.0

        # Cargar configuración desde JSON antes de inicializar imágenes
        settings = load_settings_from_json()
        self.zoom_factor = settings.get("zoom_factor", self.zoom_factor)

        # Lista de imágenes y control de índice
        self.image_list = image_list  
        self.image_index = 0  # Índice inicial

        # Intentar cargar el fondo guardado
        background_path = settings.get("background")
        if background_path and os.path.exists(background_path):
            self.image_path = background_path
        else:
            self.image_path = self.image_list[self.image_index]  # Imagen por defecto

        self.image_id = None  
        self.set_background(self.image_path)  # Aplicar la imagen correcta

        # Eventos del canvas
        self.canvas.bind("<MouseWheel>", self.on_mouse_scroll)  
        self.canvas.bind("<ButtonPress-1>", self.start_move)  
        self.canvas.bind("<B1-Motion>", self.on_drag)  
        self.canvas.bind("<Motion>", self.track_coordinates)  
        self.canvas.bind("<Button-3>", self.mostrar_menu)  

        # Crear menú contextual
        self.menu = tk.Menu(self.canvas, tearoff=0, bg=C_fondo, fg="white")

        # Submenú "Add items"
        submenu_items = tk.Menu(self.menu, tearoff=0, bg=C_fondo, fg="white")
        submenu_items.add_command(label="Add Device", command=lambda: print("add_device"))
        self.menu.add_cascade(label="Add items", menu=submenu_items)

        # Opción para cambiar el fondo
        self.menu.add_command(label="change Background", command=self.change_background)

        # Etiqueta para coordenadas del cursor
        self.coord_label = tk.Label(self, text="X: 0, Y: 0", bg=C_fondo, fg="white")
        self.coord_label.pack(side="bottom", anchor="w", padx=10, pady=5)

    def mostrar_menu(self, event):
        """Muestra el menú contextual en la posición del cursor."""
        self.menu.post(event.x_root, event.y_root)

    def track_coordinates(self, event):
        """Actualiza y muestra las coordenadas del cursor en el canvas."""
        x_canvas = self.canvas.canvasx(event.x)
        y_canvas = self.canvas.canvasy(event.y)
        self.coord_label.config(text=f"X: {int(x_canvas)}, Y: {int(y_canvas)}")

    def update_image(self, zoom_x=None, zoom_y=None):
        """Redimensiona la imagen y la actualiza en el canvas."""
        if not hasattr(self, "img_original"):
            return  

        width = int(self.img_original.width * self.zoom_factor)
        height = int(self.img_original.height * self.zoom_factor)
        resized_img = self.img_original.resize((width, height), Image.LANCZOS)
        self.img_tk = ImageTk.PhotoImage(resized_img)

        if self.image_id:
            self.canvas.delete(self.image_id)

        self.image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.img_tk)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def set_background(self, new_image_path):
        """Cambia dinámicamente el fondo del canvas y lo guarda en JSON."""
        try:
            if not new_image_path:
                return
            
            self.img_original = Image.open(new_image_path)  
            self.image_path = new_image_path
            self.update_image()

            # Guardar en JSON usando la función reutilizable
            save_setting_to_json("background", self.image_path)

        except Exception as e:
            print(f"Error al cargar la imagen: {e}")


    def change_background(self):
        """Cambia la imagen de fondo a la siguiente en la lista."""
        self.image_index = (self.image_index + 1) % len(self.image_list)
        new_image_path = self.image_list[self.image_index]
        self.set_background(new_image_path)

    def on_mouse_scroll(self, event):
        """Ajusta el zoom dentro de los límites establecidos y lo guarda."""
        zoom_x = self.canvas.canvasx(event.x)
        zoom_y = self.canvas.canvasy(event.y)

        if event.delta > 0:
            self.zoom_factor = min(self.max_zoom, self.zoom_factor + self.zoom_step)  
        else:
            self.zoom_factor = max(self.min_zoom, self.zoom_factor - self.zoom_step)  

        self.update_image(zoom_x, zoom_y)

        # Guardar el zoom en JSON
        save_setting_to_json("zoom_factor", self.zoom_factor)

    def start_move(self, event):
        """Registra la posición inicial del mouse para el desplazamiento."""
        self.canvas.scan_mark(event.x, event.y)

    def on_drag(self, event):
        """Permite arrastrar la imagen dentro del canvas."""
        self.canvas.scan_dragto(event.x, event.y, gain=1)

def screen_control(conn, username):
    global root, db_connection
    global left_frame, right_frame, left_toggle_button, right_toggle_button
    global left_expanded, right_expanded, center_frame

    if root is not None:
        root.destroy()

    root = tk.Tk()
    db_connection = conn

    root.title(f"Panel de Control - {username}")
    root.iconbitmap(icono_v)

    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    root.geometry(f"{ancho_pantalla}x{alto_pantalla - 50}+0+0")
    root.resizable(True, True)

    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)

    # Barra superior
    top_bar = tk.Frame(root, bg=C_fondo, height=30)
    top_bar.grid(row=0, column=0, sticky="ew")
    top_bar.grid_propagate(False)
    root.grid_rowconfigure(0, minsize=30)

    btn_Home = tk.Button(top_bar, text="Home", bg=C_fondo, fg=C_texto_blanco, bd=0)
    btn_Home.grid(row=0, column=0, padx=5, pady=0, sticky="ns")
    btn_Home.config(font=fuente)
    btn_Home.bind("<Enter>", on_enter)
    btn_Home.bind("<Leave>", on_leave)

    btn_Options = tk.Button(
        top_bar, text="Options",
        bg=C_fondo, fg=C_texto_blanco, bd=0
    )
    btn_Options.grid(row=0, column=1, padx=5, pady=0, sticky="ns")
    btn_Options.bind("<Enter>", on_enter)
    btn_Options.bind("<Leave>", on_leave)
    btn_Options.config(font=fuente)

    def opciones_menu(event):
        """Genera el menú de opciones con textos actualizados en cada apertura."""
        menu = tk.Menu(None, tearoff=0, bg=C_fondo, fg="white")

        # Submenú "Add items"
        submenu_items = tk.Menu(menu, tearoff=0, bg=C_fondo, fg="white")
        submenu_items.add_command(label="Add Device", command=lambda: Add_device(tree, center_frame, size=(50, 50)))
        menu.add_cascade(label="Add items", menu=submenu_items)

        # Opción "Background"
        menu.add_command(label="Background", command=lambda: center_frame.change_background())

        # Mostrar menú en la posición del cursor
        menu.post(event.x_root, event.y_root)


    btn_Options.bind("<Button-1>", opciones_menu)

    btn_Help = tk.Button(top_bar, text="Help", bg=C_fondo, fg=C_texto_blanco, bd=0)
    btn_Help.grid(row=0, column=2, padx=5, pady=0, sticky="ns")
    btn_Help.config(font=fuente)
    btn_Help.bind("<Enter>", on_enter)
    btn_Help.bind("<Leave>", on_leave)
    btn_Help.bind("<Button-1>", lambda event: show_submenu(event, [
        ("Documentation", lambda: print("boton Documentation")),
        ("About", lambda: print("boton About")),
        ("Support", lambda: print("boton Support"))
    ]))

    main_frame = tk.Frame(root, bg=C_fondo)
    main_frame.grid(row=1, column=0, sticky="nsew")

    left_expanded = True
    left_frame = tk.Frame(main_frame, bg=C_fondo, width=200)
    left_frame.pack(side="left", fill="y")
    left_frame.pack_propagate(False)

    left_toggle_button = tk.Button(
        left_frame, 
        text="◀", 
        command=toggle_left_bar, 
        fg="white",
        bg=C_fondo,
        width=2,
        borderwidth=0,
        highlightthickness=0
    )
    left_toggle_button.pack(side="right", fill="y")

    crear_treeview_dispositivos(left_frame, db_connection)

    center_frame = ZoomableCanvas(parent=main_frame, image_list=image_list)
    center_frame.pack(side="left", fill="both", expand=True)

    right_expanded = True
    right_frame = tk.Frame(main_frame, bg=C_fondo, width=200)
    right_frame.pack(side="right", fill="y")
    right_frame.pack_propagate(False)

    right_toggle_button = tk.Button(
        right_frame, 
        text="▶", 
        command=toggle_right_bar, 
        fg="white",
        bg=C_fondo,
        width=2,
        borderwidth=0,
        highlightthickness=0
    )
    right_toggle_button.pack(side="left", fill="y")

    bottom_bar = tk.Frame(root, bg=C_fondo, height=20)
    bottom_bar.grid(row=2, column=0, sticky="ew")
    root.grid_rowconfigure(2, minsize=20)

    status_label = tk.Label(bottom_bar, text="Listo", bg=C_fondo, fg=C_texto_blanco)
    status_label.pack(side="left", padx=10)

    root.mainloop()

def obtener_dispositivos(conn):
    query = "SELECT nombre, ip, tipo FROM dispositivos ORDER BY nombre;"
    cursor = conn.cursor()
    cursor.execute(query)
    dispositivos = cursor.fetchall()
    cursor.close()

    #print("DEBUG - Datos obtenidos de la BD:", dispositivos)  # Verifica qué devuelve la BD

    return dispositivos

def organizar_dispositivos_por_prefijo(dispositivos):
    estructura = {}

    for nombre, ip, tipo in dispositivos:
        prefijo = nombre.split("_")[0]  # Tomamos el prefijo de la ciudad
        categoria = "Routers" if "_R" in nombre else "Switches"

        if prefijo not in estructura:
            estructura[prefijo] = {}
        if categoria not in estructura[prefijo]:
            estructura[prefijo][categoria] = []

        estructura[prefijo][categoria].append((nombre, ip))  # Guardamos en tupla (nombre, ip)
    
    return estructura

def filtrar_treeview(tree, estructura, query):
    """ Filtra los elementos en el Treeview en función de la búsqueda. """
    query = query.strip().lower()
    tree.delete(*tree.get_children())  # Limpiar Treeview

    if not query:  # Si no hay búsqueda, restaurar la lista completa
        poblar_treeview(tree, estructura)
        return

    total_filas = 0
    for prefijo, categorias in estructura.items():
        prefijo_id = None

        for categoria, equipos in categorias.items():
            categoria_id = None

            for nombre, ip in equipos:
                if query in nombre.lower() or query in ip:
                    if prefijo_id is None:
                        prefijo_id = tree.insert("", "end", text=prefijo, open=True)
                    if categoria_id is None:
                        categoria_id = tree.insert(prefijo_id, "end", text=categoria, open=True)

                    tree.insert(categoria_id, "end", text=f"{nombre} ({ip})")
                    total_filas += 1

    # Si no hay coincidencias, mostrar un mensaje temporal
    if total_filas == 0:
        tree.insert("", "end", text="No se encontraron resultados")

def poblar_treeview(tree, estructura):
    """ Llena el Treeview con todos los dispositivos. """
    for prefijo, categorias in estructura.items():
        prefijo_id = tree.insert("", "end", text=prefijo, open=True)

        for categoria, equipos in categorias.items():
            if equipos:
                categoria_id = tree.insert(prefijo_id, "end", text=categoria, open=True)

                for equipo in equipos:
                    #print("DEBUG - Equipo:", equipo)  # Verifica qué estructura tiene

                    if isinstance(equipo, tuple) and len(equipo) == 2:
                        nombre, ip = equipo
                        tree.insert(categoria_id, "end", text=f"{nombre} ({ip})")  # <- AQUÍ CONCATENAMOS CORRECTAMENTE
                    else:
                        return
                        #print("ERROR: El equipo no tiene la estructura esperada:", equipo)

def crear_treeview_dispositivos(parent, conn):
    global tree

    dispositivos = obtener_dispositivos(conn)
    estructura = organizar_dispositivos_por_prefijo(dispositivos)

    # Configurar el fondo del contenedor principal
    parent.config(bg=C_fondo)

    # Crear un marco principal
    main_frame = tk.Frame(parent, bg=C_fondo)
    main_frame.pack(fill="both", expand=True)

    # Cuadro de búsqueda
    search_var = tk.StringVar()
    search_entry = tk.Entry(
        main_frame, 
        textvariable=search_var, 
        fg=C_texto_Azul, 
        bg=C_fondo, 
        justify="center", 
        font=(fuente)
    )
    search_entry.insert(0, "Type to search...")
    
    def on_entry_click(event):
        if search_entry.get() == "Type to search...":
            search_entry.delete(0, tk.END)
            search_entry.config(fg=C_texto_Azul)
    
    def on_focus_out(event):
        if not search_var.get().strip():
            search_entry.insert(0, "Type to search...")
            search_entry.config(fg=C_texto_Azul)
            filtrar_treeview(tree, estructura, "")
    
    search_entry.bind("<FocusIn>", on_entry_click)
    search_entry.bind("<FocusOut>", on_focus_out)
    search_entry.pack(fill="x", padx=10, pady=10)
    
    # Frame para el Treeview
    tree_frame = tk.Frame(main_frame, bg=C_fondo)
    tree_frame.pack(fill="both", expand=True)

    # Configurar el estilo del Treeview
    style = ttk.Style()
    style.configure("Treeview", 
        background=C_fondo, 
        fieldbackground=C_fondo,
        foreground=C_texto_blanco,
        rowheight=30,
        borderwidth=0
    )
    style.map("Treeview", background=[("selected", C_fondo_2)])
    
    # Crear el Treeview
    tree = ttk.Treeview(tree_frame, columns=("Nombre",), show="tree")
    tree.column("#0", minwidth=300, width=350, stretch=True)
    tree.heading("#0", text="Dispositivos")
    
    # Asegurar que el fondo de cada fila coincida con el del Treeview
    tree.tag_configure("evenrow", background=C_fondo)
    tree.tag_configure("oddrow", background=C_fondo)
    
    tree.grid(row=0, column=0, sticky="nsew")
    tree_frame.columnconfigure(0, weight=1)
    tree_frame.rowconfigure(0, weight=1)
    
    # Llenar Treeview
    poblar_treeview(tree, estructura)
    
    # Filtrar al escribir
    search_var.trace_add("write", lambda *args: filtrar_treeview(tree, estructura, search_var.get()))
    
    # Menú contextual
    menu = tk.Menu(tree, tearoff=0)
    menu.configure(
    background=C_fondo,  # Color de fondo del menú
    foreground=C_texto_blanco,   # Color del texto (opcional, no siempre se aplica)
    activebackground=C_fondo_2,  # Color cuando se pasa el mouse
    )
    menu.add_command(label="Ver detalles", command=lambda: ver_detalles(tree, center_frame, icono_v))
    menu.add_command(label="Add Device", command=lambda: Add_device(tree, center_frame, size=(50, 50)))
    menu.add_command(label="Eliminar", command=lambda: print("Eliminar"))
    
    def mostrar_menu(event):
        item = tree.identify_row(event.y)
        if item:
            tree.selection_set(item)
            menu.post(event.x_root, event.y_root)
    
    tree.bind("<Button-3>", mostrar_menu)
    
    return tree