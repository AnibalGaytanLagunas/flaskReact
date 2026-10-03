from utils.db import mysql
from exceptions.product_exceptions import *

def get_all_products():    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    columnas = [columna[0] for columna in cursor.description]
    result = [
        dict(zip(columnas, product))
        for product in products
    ]
    cursor.close()
    ##Forma desarrollada 
    ##result_d = [{
    ##  "id": product[0],
    ##  "name": product[1],
    ##  "price": product[2],
    ##  "description": product[3]
    ##} for product in products ]              
    ##fin forma desarrollada
    return result


def create_product(name, price, description):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO products(name, price, description)VALUES (%s, %s, %s)", (name, price, description))
    mysql.connection.commit()
    product_id = cursor.lastrowid
    cursor.close()
    return product_id


def get_product_by_id(product_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products WHERE id = %s",(product_id,))
    product = cursor.fetchone()
    cursor.close()
    return product


def update_product(product_id, name, price, description):
    cursor = mysql.connection.cursor()
    cursor.execute( " UPDATE products SET name = %s, price = %s, description = %s WHERE id = %s", (name, price, description, product_id))
    mysql.connection.commit()
    cursor.close()


def delete_product(product_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    mysql.connection.commit()
    cursor.close()