-- Run this once in MySQL before scripts/import_to_mysql.py
CREATE DATABASE IF NOT EXISTS sales_analysis;
USE sales_analysis;

CREATE TABLE IF NOT EXISTS superstore (
    row_id        INT PRIMARY KEY,
    order_id      VARCHAR(20),
    order_date    DATE,
    ship_date     DATE,
    ship_mode     VARCHAR(20),
    customer_id   VARCHAR(20),
    customer_name VARCHAR(60),
    segment       VARCHAR(20),
    country       VARCHAR(40),
    city          VARCHAR(60),
    state         VARCHAR(40),
    postal_code   VARCHAR(10),
    region        VARCHAR(20),
    product_id    VARCHAR(20),
    category      VARCHAR(30),
    sub_category  VARCHAR(30),
    product_name  VARCHAR(255),
    sales         DECIMAL(12,4),
    quantity      INT,
    discount      DECIMAL(4,2),
    profit        DECIMAL(12,4)
);
