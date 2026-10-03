-- insertar manualmente los comando en Mysql o investigar como automatizarlos

CREATE DATABASE IF NOT EXISTS restaurantdb;

-- Seleccionar la base de datos
USE restaurantdb;

-- Crear la tabla productos y insertarlos
CREATE TABLE products (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(30) NOT NULL, price DECIMAL(10, 2) NOT NULL, description VARCHAR(255));
INSERT INTO products (name, price, description) VALUES('Enbutido', 125.00, 'Pastel de carne con cerdo molido, huevo duro, queso cheddar, pimiento y zanahoria'),('Kare', 125.00, 'Cola de res en salsa, mantequilla de cacahuate, achiote, verduras'),('Lumpias', 125.00, 'Lumpias frescas con salsa de cacahuate, crepa de harina, verduras, germinado, mantequilla de cacahuate'),('Menudo', 125.00, 'Menudo filipino con cerdo, hígado, papa, zanahoria, salsa de tomate y pasitas'),('Panza', 125.00, 'Panza de cerdo a la parrilla, salsa de soya, catsup, ajo, limón'),('Robalo', 125.00, 'Robalo relleno entero, zanahoria, chícharos, pasitas y salsa de ostión');