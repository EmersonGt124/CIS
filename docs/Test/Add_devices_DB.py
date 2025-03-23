import random
import psycopg2
from datetime import datetime, timedelta

# Conexión a PostgreSQL
conn = psycopg2.connect(
    dbname="isp_networks",
    user="isp_admin",
    password="isp_admin123",
    host="127.0.0.1",
    port="5432"
)
cursor = conn.cursor()

# Borrar todos los datos antes de insertar nuevos
cursor.execute("DELETE FROM dispositivos")
conn.commit()

# Listas de datos
ciudades = ["MEDELLIN", "CALI", "BARRANQUILLA", "BOGOTA", "BUCARAMANGA"]
tipos = {"Switch": "S", "Router": "R"}
modelos_fabricantes = {
    "NokiaSR7750": "Nokia",
    "HuaweiS720": "Huawei",
    "Cisco3850": "Cisco",
    "Nokia7250": "Nokia",
    "HuaweiNE40": "Huawei",
    "Cisco6500": "Cisco"
}
ubicaciones = ["Data Center", "Sala de Comunicaciones", "Oficina Principal", "Sucursal"]
estados = ["Activo", "Inactivo"]

# Obtener IPs ya existentes en la base de datos
cursor.execute("SELECT ip FROM dispositivos")
ips_existentes = {row[0] for row in cursor.fetchall()}

# Generar 200 registros sin duplicar IPs
nuevas_ips = set()
for _ in range(200):
    ciudad = random.choice(ciudades)
    tipo_nombre, tipo_abreviado = random.choice(list(tipos.items()))
    modelo, fabricante = random.choice(list(modelos_fabricantes.items()))
    nombre = f"{ciudad[:3]}_{modelo}_{tipo_abreviado}"  # Nuevo formato

    # Generar IP única
    while True:
        ip = f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
        if ip not in ips_existentes and ip not in nuevas_ips:
            nuevas_ips.add(ip)
            break  # Sale del bucle cuando encuentra una IP única

    ubicacion = random.choice(ubicaciones)
    fecha_instalacion = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1500))
    estado = random.choice(estados)

    # Insertar en la base de datos
    cursor.execute(
        """
        INSERT INTO dispositivos (nombre, ip, tipo, modelo, fabricante, ubicacion, fecha_instalacion, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (nombre, ip, tipo_nombre, modelo, fabricante, ubicacion, fecha_instalacion, estado)
    )

# Confirmar cambios y cerrar conexión
conn.commit()
cursor.close()
conn.close()

print("Se han insertado 200 registros con el nuevo formato sin repetir IPs.")
