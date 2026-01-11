-- ===============================
-- DIMENSIONES
-- ===============================

CREATE TABLE dim_customer (
    customer_id SERIAL PRIMARY KEY,
    email TEXT,
    registration_date DATE,
    customer_segment TEXT,
    total_orders INT,
    lifetime_value DECIMAL(12,2)
);

CREATE TABLE dim_product (
    product_id SERIAL PRIMARY KEY,
    sku TEXT,
    name TEXT,
    category TEXT,
    brand TEXT,
    unit_cost DECIMAL(10,2),
    current_price DECIMAL(10,2)
);

CREATE TABLE dim_time (
    date_key INT PRIMARY KEY,
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    day_of_week INT,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
);

CREATE TABLE dim_location (
    location_id SERIAL PRIMARY KEY,
    country TEXT,
    region TEXT,
    city TEXT,
    postal_code TEXT,
    timezone TEXT
);

-- ===============================
-- TABLA DE HECHOS
-- ===============================

CREATE TABLE fact_orders (
    order_id BIGINT PRIMARY KEY,
    customer_id INT REFERENCES dim_customer(customer_id),
    product_id INT REFERENCES dim_product(product_id),
    time_id INT REFERENCES dim_time(date_key),
    location_id INT REFERENCES dim_location(location_id),

    quantity_ordered INT,
    unit_price DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    shipping_cost DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    profit_margin DECIMAL(10,2),
    is_first_purchase BOOLEAN,
    order_channel TEXT,
    payment_method TEXT
);

-- ===============================
-- ÍNDICES ANALÍTICOS
-- ===============================

CREATE INDEX idx_fact_orders_time ON fact_orders(time_id);
CREATE INDEX idx_fact_orders_product ON fact_orders(product_id);
CREATE INDEX idx_fact_orders_customer ON fact_orders(customer_id);
CREATE INDEX idx_dim_time_year_month ON dim_time(year, month);

-- ===============================
-- VISTAS
-- ===============================

CREATE VIEW product_performance AS
SELECT
    dp.name AS product_name,
    dp.category,
    dp.brand,
    SUM(fo.quantity_ordered) AS total_units_sold,
    SUM(fo.total_amount) AS total_revenue,
    AVG(fo.unit_price) AS avg_selling_price,
    COUNT(DISTINCT fo.customer_id) AS unique_customers,
    ROW_NUMBER() OVER (
        PARTITION BY dp.category
        ORDER BY SUM(fo.total_amount) DESC
    ) AS category_rank
FROM fact_orders fo
JOIN dim_product dp ON fo.product_id = dp.product_id
JOIN dim_time dt ON fo.time_id = dt.date_key
WHERE dt.year = 2024
GROUP BY dp.product_id, dp.name, dp.category, dp.brand;

CREATE MATERIALIZED VIEW executive_dashboard AS
SELECT
    dt.year,
    dt.month,
    SUM(fo.total_amount) AS monthly_revenue,
    COUNT(DISTINCT fo.customer_id) AS active_customers,
    COUNT(fo.order_id) AS total_orders,
    AVG(fo.total_amount) AS avg_order_value,
    (SUM(fo.total_amount) -
     LAG(SUM(fo.total_amount)) OVER (ORDER BY dt.year, dt.month)) /
     NULLIF(LAG(SUM(fo.total_amount)) OVER (ORDER BY dt.year, dt.month), 0)
     AS growth_rate
FROM fact_orders fo
JOIN dim_time dt ON fo.time_id = dt.date_key
GROUP BY dt.year, dt.month
ORDER BY dt.year, dt.month;
