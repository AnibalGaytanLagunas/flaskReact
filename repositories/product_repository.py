"""Acceso a datos para el recurso de productos."""

import sys

from utils.db import mysql


def _close_cursor(cursor):
    """Cierra el cursor sin ocultar una excepción original."""
    if cursor is None:
        return

    # Capturar el estado antes de llamar a close(): dentro del except de
    # cursor.close(), sys.exc_info() reflejaría el error de cierre, no el
    # error que pudiera estar propagándose desde la operación principal.
    preserve_error = sys.exc_info()[0] is not None

    try:
        cursor.close()
    except Exception:
        if not preserve_error:
            raise


def _rollback_preserving_error(connection):
    """Intenta revertir la transacción sin ocultar el error original."""
    try:
        connection.rollback()
    except Exception:
        pass


def get_all_products():
    cursor = None

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM products")

        products = cursor.fetchall()
        columns = [column[0] for column in cursor.description]

        return [
            dict(zip(columns, product))
            for product in products
        ]
    finally:
        _close_cursor(cursor)


def create_product(name, price, description):
    connection = mysql.connection
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO products (name, price, description)
            VALUES (%s, %s, %s)
            """,
            (name, price, description),
        )

        product_id = cursor.lastrowid
        connection.commit()
        return product_id

    except Exception:
        _rollback_preserving_error(connection)
        raise

    finally:
        _close_cursor(cursor)


def get_product_by_id(product_id):
    cursor = None

    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM products WHERE id = %s",
            (product_id,),
        )
        return cursor.fetchone()

    finally:
        _close_cursor(cursor)


def update_product(product_id, name, price, description):
    """
    Actualiza un producto dentro de una única transacción.

    SELECT ... FOR UPDATE bloquea la fila hasta el commit/rollback,
    evitando que otro proceso elimine o modifique el producto entre
    la comprobación de existencia y el UPDATE.
    """
    connection = mysql.connection
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id
            FROM products
            WHERE id = %s
            FOR UPDATE
            """,
            (product_id,),
        )

        product = cursor.fetchone()

        if product is None:
            connection.rollback()
            return False

        cursor.execute(
            """
            UPDATE products
            SET name = %s,
                price = %s,
                description = %s
            WHERE id = %s
            """,
            (name, price, description, product_id),
        )

        connection.commit()
        return True

    except Exception:
        _rollback_preserving_error(connection)
        raise

    finally:
        _close_cursor(cursor)


def delete_product(product_id):
    """
    Elimina un producto dentro de una única transacción.

    SELECT ... FOR UPDATE garantiza que la comprobación de existencia
    y el DELETE formen parte de la misma unidad transaccional.
    """
    connection = mysql.connection
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id
            FROM products
            WHERE id = %s
            FOR UPDATE
            """,
            (product_id,),
        )

        product = cursor.fetchone()

        if product is None:
            connection.rollback()
            return False

        cursor.execute(
            "DELETE FROM products WHERE id = %s",
            (product_id,),
        )

        connection.commit()
        return True

    except Exception:
        _rollback_preserving_error(connection)
        raise

    finally:
        _close_cursor(cursor)
