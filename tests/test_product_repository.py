"""Pruebas unitarias para el repositorio de productos."""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from repositories import product_repository


@pytest.fixture
def db(monkeypatch):
    connection = MagicMock()
    cursor = MagicMock()
    connection.cursor.return_value = cursor

    mysql_mock = SimpleNamespace(connection=connection)
    monkeypatch.setattr(product_repository, "mysql", mysql_mock)

    return connection, cursor


def test_get_all_products_returns_dictionaries(db):
    _, cursor = db
    cursor.description = [("id",), ("name",), ("price",), ("description",)]
    cursor.fetchall.return_value = [(1, "Tacos", 50.0, "Tacos de cecina")]

    result = product_repository.get_all_products()

    assert result == [{
        "id": 1,
        "name": "Tacos",
        "price": 50.0,
        "description": "Tacos de cecina",
    }]
    cursor.close.assert_called_once()


def test_get_all_products_closes_cursor_on_error(db):
    _, cursor = db
    cursor.execute.side_effect = RuntimeError("Error SQL")

    with pytest.raises(RuntimeError, match="Error SQL"):
        product_repository.get_all_products()

    cursor.close.assert_called_once()


def test_get_product_by_id_uses_parameterized_query(db):
    _, cursor = db
    cursor.fetchone.return_value = (5, "Tacos", 50.0, "Cecina")

    result = product_repository.get_product_by_id(5)

    cursor.execute.assert_called_once_with(
        "SELECT * FROM products WHERE id = %s",
        (5,),
    )
    assert result == (5, "Tacos", 50.0, "Cecina")
    cursor.close.assert_called_once()


def test_create_product_commits_and_closes_cursor(db):
    connection, cursor = db
    cursor.lastrowid = 12

    result = product_repository.create_product("Tacos", 50.0, "Tacos de cecina")

    assert result == 12
    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()
    cursor.close.assert_called_once()


def test_create_product_rolls_back_on_error(db):
    connection, cursor = db
    cursor.execute.side_effect = RuntimeError("Error SQL")

    with pytest.raises(RuntimeError, match="Error SQL"):
        product_repository.create_product("Tacos", 50.0, "Tacos de cecina")

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    cursor.close.assert_called_once()


def test_update_product_locks_row_and_commits(db):
    connection, cursor = db
    cursor.fetchone.return_value = (5,)

    result = product_repository.update_product(
        5, "Tacos", 50.0, "Tacos de cecina"
    )

    assert result is True
    assert cursor.execute.call_count == 2

    first_query = cursor.execute.call_args_list[0]
    second_query = cursor.execute.call_args_list[1]

    assert "FOR UPDATE" in first_query.args[0]
    assert first_query.args[1] == (5,)
    assert "UPDATE products" in second_query.args[0]
    assert second_query.args[1] == ("Tacos", 50.0, "Tacos de cecina", 5)

    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()
    cursor.close.assert_called_once()


def test_update_product_returns_false_when_product_does_not_exist(db):
    connection, cursor = db
    cursor.fetchone.return_value = None

    result = product_repository.update_product(
        5, "Tacos", 50.0, "Tacos de cecina"
    )

    assert result is False
    assert cursor.execute.call_count == 1
    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    cursor.close.assert_called_once()


def test_update_product_rolls_back_on_error(db):
    connection, cursor = db
    cursor.fetchone.return_value = (5,)
    cursor.execute.side_effect = [None, RuntimeError("Error SQL")]

    with pytest.raises(RuntimeError, match="Error SQL"):
        product_repository.update_product(
            5, "Tacos", 50.0, "Tacos de cecina"
        )

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    cursor.close.assert_called_once()


def test_delete_product_locks_row_and_commits(db):
    connection, cursor = db
    cursor.fetchone.return_value = (5,)

    result = product_repository.delete_product(5)

    assert result is True
    assert cursor.execute.call_count == 2

    first_query = cursor.execute.call_args_list[0]
    second_query = cursor.execute.call_args_list[1]

    assert "FOR UPDATE" in first_query.args[0]
    assert first_query.args[1] == (5,)
    assert second_query.args[0] == "DELETE FROM products WHERE id = %s"
    assert second_query.args[1] == (5,)

    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()
    cursor.close.assert_called_once()


def test_delete_product_returns_false_when_product_does_not_exist(db):
    connection, cursor = db
    cursor.fetchone.return_value = None

    result = product_repository.delete_product(5)

    assert result is False
    assert cursor.execute.call_count == 1
    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    cursor.close.assert_called_once()


def test_delete_product_rolls_back_on_error(db):
    connection, cursor = db
    cursor.fetchone.return_value = (5,)
    cursor.execute.side_effect = [None, RuntimeError("Error SQL")]

    with pytest.raises(RuntimeError, match="Error SQL"):
        product_repository.delete_product(5)

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    cursor.close.assert_called_once()


def test_create_product_preserves_original_error_if_rollback_fails(db):
    connection, cursor = db
    cursor.execute.side_effect = RuntimeError("Error SQL")
    connection.rollback.side_effect = RuntimeError("Error rollback")

    with pytest.raises(RuntimeError, match="Error SQL"):
        product_repository.create_product("Tacos", 50.0, "Tacos de cecina")

    cursor.close.assert_called_once()


def test_cursor_close_error_does_not_replace_active_exception(db):
    _, cursor = db
    cursor.execute.side_effect = RuntimeError("Error SQL")
    cursor.close.side_effect = RuntimeError("Error close")

    with pytest.raises(RuntimeError, match="Error SQL"):
        product_repository.get_all_products()


def test_cursor_close_error_is_propagated_without_active_exception(db):
    _, cursor = db
    cursor.close.side_effect = RuntimeError("Error close")

    with pytest.raises(RuntimeError, match="Error close"):
        product_repository.get_all_products()
