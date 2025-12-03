BEGIN TRANSACTION;

INSERT INTO clientes (nombre, email, fecha_registro)
VALUES ('Cristian', 'c@pc.com', '2025-11-24');

INSERT INTO pedidos (cliente_id, fecha_pedido, total)
VALUES (last_insert_rowid(), '2025-11-24', 500.0);

COMMIT;

DROP TABLE IF EXISTS productos;

CREATE TABLE productos (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    categoria TEXT,
    stock INTEGER DEFAULT 0
);

INSERT INTO productos VALUES
(1, 'Laptop Dell', 1200.00, 'Electrónica', 15),
(2, 'Mouse Logitech', 25.50, 'Accesorios', 50),
(3, 'Teclado Mecánico', 89.99, 'Accesorios', 30),
(4, 'Monitor 24"', 199.99, 'Electrónica', 12),
(5, 'Audífonos Sony', 149.50, 'Audio', 25);

-- Seleccionar productos con precio > 100
SELECT nombre, precio FROM productos WHERE precio > 100;

-- Productos de categoría 'Electrónica' ordenados por precio descendente
SELECT nombre, precio, categoria FROM productos
WHERE categoria = 'Electrónica'
ORDER BY precio DESC;

-- Nombres que contienen 'a' ordenados alfabéticamente
SELECT nombre, precio FROM productos
WHERE nombre LIKE '%a%'
ORDER BY nombre ASC;

SELECT nombre, precio FROM productos
WHERE nombre LIKE '%s%'
ORDER BY nombre ASC;

-- Ejercicios semana 2 día 3
DROP TABLE IF EXISTS clientes;

-- Tabla de clientes
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE,
    ciudad TEXT
);

DROP TABLE IF EXISTS pedidos;

-- Tabla de pedidos
CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER,
    fecha_pedido DATE NOT NULL,
    total REAL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

INSERT INTO clientes VALUES
(1, 'Ana García', 'ana@email.com', 'Madrid'),
(2, 'Carlos López', 'carlos@email.com', 'Barcelona'),
(3, 'María Rodríguez', 'maria@email.com', 'Madrid');

INSERT INTO pedidos VALUES
(1, 1, '2024-01-15', 150.50),
(2, 1, '2024-01-20', 89.99),
(3, 2, '2024-01-18', 299.99);

-- INNER JOIN: Solo clientes con pedidos
SELECT c.nombre, p.fecha_pedido, p.total
FROM clientes c
INNER JOIN pedidos p ON c.id = p.cliente_id;

-- LEFT JOIN: Todos los clientes, con pedidos si existen
SELECT c.nombre, COUNT(p.id) as num_pedidos, SUM(p.total) as total_compras
FROM clientes c
LEFT JOIN pedidos p ON c.id = p.cliente_id
GROUP BY c.id, c.nombre;

-- Clientes de Madrid con sus pedidos
SELECT c.nombre, c.ciudad, p.fecha_pedido, p.total
FROM clientes c
LEFT JOIN pedidos p ON c.id = p.cliente_id
WHERE c.ciudad = 'Madrid';

-- Funciones de Agregación y GROUP BY - Día 4

-- Tabla de detalles de pedidos
CREATE TABLE detalle_pedidos (
    id INTEGER PRIMARY KEY,
    pedido_id INTEGER,
    producto_id INTEGER,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Insertar datos de ejemplo
INSERT INTO detalle_pedidos VALUES
(1, 1, 1, 1, 1200.00),
(2, 1, 2, 2, 25.50),
(3, 2, 3, 1, 89.99),
(4, 3, 4, 1, 199.99),
(5, 3, 5, 1, 149.50);

-- Consultas de agregación básica:

-- Ventas totales por producto
SELECT producto_id, SUM(cantidad) as total_vendido, SUM(cantidad * precio_unitario) as ingresos_totales
FROM detalle_pedidos
GROUP BY producto_id;

-- Estadísticas por pedido
SELECT pedido_id, COUNT(*) as items_diferentes, SUM(cantidad) as cantidad_total, AVG(precio_unitario) as precio_promedio
FROM detalle_pedidos
GROUP BY pedido_id;

-- Consultas con HAVING:

-- Productos con más de 1 unidad vendida total
SELECT producto_id, SUM(cantidad) as total_vendido
FROM detalle_pedidos
GROUP BY producto_id
HAVING SUM(cantidad) > 1;

-- Pedidos con valor total > 150
SELECT pedido_id, SUM(cantidad * precio_unitario) as valor_total
FROM detalle_pedidos
GROUP BY pedido_id
HAVING SUM(cantidad * precio_unitario) > 150;

-- Análisis combinado con joins:

-- Ventas por ciudad usando JOIN + GROUP BY
SELECT c.ciudad, COUNT(p.id) as num_pedidos, SUM(dp.cantidad * dp.precio_unitario) as ingresos_ciudad
FROM clientes c
LEFT JOIN pedidos p ON c.id = p.cliente_id
LEFT JOIN detalle_pedidos dp ON p.id = dp.pedido_id
GROUP BY c.ciudad
HAVING SUM(dp.cantidad * dp.precio_unitario) > 0;