import pandas as pd
import numpy as np

# Dataset de ventas
ventas = pd.DataFrame({
    'id_venta': range(1, 11),
    'id_cliente': np.random.choice([1, 2, 3, 4, 5], 10),
    'id_producto': np.random.choice([101, 102, 103, 104], 10),
    'cantidad': np.random.randint(1, 5, 10),
    'fecha': pd.date_range('2024-01-01', periods=10, freq='D')
})

# Dataset de clientes
clientes = pd.DataFrame({
    'id_cliente': [1, 2, 3, 4, 5],
    'nombre': ['Ana', 'Carlos', 'María', 'Juan', 'Luis'],
    'ciudad': ['Madrid', 'Barcelona', 'Madrid', 'Valencia', 'Sevilla']
})

# Dataset de productos
productos = pd.DataFrame({
    'id_producto': [101, 102, 103, 104],
    'nombre': ['Laptop', 'Mouse', 'Teclado', 'Monitor'],
    'precio': [1200, 25, 80, 300],
    'categoria': ['Electrónica', 'Accesorios', 'Accesorios', 'Electrónica']
})

print("Datasets creados:")
print(f"Ventas: {ventas.shape}")
print(f"Clientes: {clientes.shape}")
print(f"Productos: {productos.shape}")

# Ventas del mes actual con query
ventas_recientes = ventas.query('fecha >= "2024-01-05"')
print(f"\nVentas recientes: {len(ventas_recientes)}")

# Productos caros usando variable externa
precio_limite = 100
productos_caros = productos.query('precio >= @precio_limite')
print(f"Productos caros (>= {precio_limite}): {productos_caros['nombre'].tolist()}")

# Ventas por producto
ventas_por_producto= ventas.groupby('id_producto')['cantidad'].sum()
print(f"\nVentas por producto:\n{ventas_por_producto}")

# Estadísticas por cliente
stats_por_cliente= ventas.groupby('id_cliente').agg({
'cantidad':['sum','mean'],
'id_venta':'count'
})
print(f"\nEstadísticas por cliente:\n{stats_por_cliente}")

# Unir ventas con productos
ventas_productos= pd.merge(ventas, productos, on='id_producto')

# Calcular totales
ventas_productos['total']= ventas_productos['cantidad']* ventas_productos['precio']

# Unir con clientes
analisis_completo= pd.merge(ventas_productos, clientes, on='id_cliente')
analisis_completo = analisis_completo.rename(columns={
    'nombre_x': 'producto',
    'nombre_y': 'cliente'
})

print(f"\nAnálisis completo (primeras 5 filas):\n{analisis_completo.head()}")

# Análisis por ciudad
ventas_por_ciudad= analisis_completo.groupby('ciudad')['total'].sum()
print(f"\nVentas totales por ciudad:\n{ventas_por_ciudad}")

# Clientes con compras > 1000
clientes_top = analisis_completo.groupby(['id_cliente','cliente'])['total'].sum()
clientes_top = clientes_top[clientes_top > 1000]
print(f"\nClientes con compras > 1000:\n{clientes_top}")

