import csv

def leer_csv(ruta_archivo):
    datos = []
    with open(ruta_archivo, 'r') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            datos.append(fila)
    return datos

# Uso
clientes = leer_csv('clientes.csv')
print(f"Leídos {len(clientes)} clientes")

""" import json

def extraer_api_simulada():
    # Simular respuesta de API
    datos_api = {
        "productos": [
            {"id": 1, "nombre": "Producto A", "precio": 100},
            {"id": 2, "nombre": "Producto B", "precio": 200}
        ]
    }
    return datos_api["productos"]

productos = extraer_api_simulada()
print(f"Extraídos {len(productos)} productos") """

""" import sqlite3

def conectar_base_datos():
    conn = sqlite3.connect(':memory:')  # Base temporal
    cursor = conn.cursor()
    
    # Crear tabla
    cursor.execute('''
        CREATE TABLE ventas (
            id INTEGER PRIMARY KEY,
            producto TEXT,
            cantidad INTEGER
        )
    ''')
    
    # Insertar datos de ejemplo
    cursor.execute("INSERT INTO ventas VALUES (1, 'Producto A', 10)")
    cursor.execute("INSERT INTO ventas VALUES (2, 'Producto B', 5)")
    
    # Leer datos
    cursor.execute("SELECT * FROM ventas")
    resultados = cursor.fetchall()
    
    conn.close()
    return resultados

ventas = conectar_base_datos()
print(f"Encontradas {len(ventas)} ventas") """

# VERIFICACIÓN
# Verificación: 
# 1. ¿Qué consideraciones de seguridad debes tener al conectar con bases de datos y APIs?
# 2. ¿Cómo manejarías errores de conexión o respuestas inválidas?

# RESPUESTAS
# 1. Consideraciones de seguridad al conectar con bases de datos y APIs

# Bases de datos

#- Nunca hardcodear credenciales (usuario, contraseña) en el código; usar variables de entorno.

#- Principio de mínimo privilegio: el usuario de BD debe tener solo permisos necesarios.

#- Consultas parametrizadas para evitar SQL Injection.

#- Cifrado: usar conexiones seguras cuando aplique (SSL/TLS en BDs reales).

# APIs

#- Proteger API keys y tokens (no subirlos a repositorios).

#- Usar HTTPS siempre.

#- Validar el origen y formato de la respuesta (JSON esperado).

#- Implementar rate limiting y control de acceso si se consume una API propia.


# 2. Manejo de errores de conexión o respuestas inválidas

# Estrategia general:

#- Usar bloques try / except para capturar errores.

#- Diferenciar errores:

#-    - conexión

#-    - formato de datos

#-    - respuesta vacía o incompleta

#- Registrar errores (logs) en lugar de detener el programa.