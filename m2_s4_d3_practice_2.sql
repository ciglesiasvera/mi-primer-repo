-- Estrategias de particionamiento para diferentes componentes
CREATE DATABASE bd_analisis_big_data;
-- 1. Eventos de usuario (streaming + histórico)
-- Kafka topics particionados por tipo de evento
CREATE TABLE eventos_usuario (
    event_time TIMESTAMP NOT NULL,
    user_id BIGINT NOT NULL,
    event_type VARCHAR(50),
    session_id VARCHAR(100),
    properties JSONB
) PARTITION BY RANGE (event_time);

CREATE TABLE eventos_usuario_2024_01
PARTITION OF eventos_usuario
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE ordenes (
    order_id BIGINT,
    user_id BIGINT,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2),
    status VARCHAR(20)
) PARTITION BY RANGE (order_date);

CREATE TABLE ordenes_2024_01
PARTITION OF ordenes
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE productos (
    product_id BIGINT PRIMARY KEY,
    category_id INTEGER,
    name VARCHAR(200),
    price DECIMAL(10,2),
    stock_quantity INTEGER
);

CREATE INDEX idx_category_price 
ON productos(category_id, price);

CREATE INDEX idx_stock 
ON productos(stock_quantity)
WHERE stock_quantity > 0;

CREATE TABLE metricas_diarias (
    fecha DATE NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    ventas_total DECIMAL(10,2),
    ordenes_total INTEGER,
    clientes_unicos INTEGER,
    conversion_rate DECIMAL(5,4)
) PARTITION BY RANGE (fecha);

CREATE TABLE metricas_diarias_2024_01
PARTITION OF metricas_diarias
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Filtros temporales + agrupaciones
CREATE INDEX idx_metricas_fecha
ON metricas_diarias (fecha);

-- Consultas por categoría
CREATE INDEX idx_metricas_categoria
ON metricas_diarias (categoria);

-- Consultas por región
CREATE INDEX idx_metricas_region
ON metricas_diarias (region);

-- Consultas combinadas (muy común en dashboards)
CREATE INDEX idx_metricas_fecha_categoria_region
ON metricas_diarias (fecha, categoria, region);
