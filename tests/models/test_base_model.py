import psycopg2
import pytest
from unittest.mock import MagicMock, patch
from models.base_model import BaseModel


@pytest.fixture
def mock_db_connection():
    """提供一個模擬的資料庫連接"""
    return MagicMock()


@pytest.fixture
def base_model(mock_db_connection):
    """提供一個已初始化的 BaseModel 實例"""
    model = BaseModel(db_connection=mock_db_connection)
    model.table_name = "test_table"
    return model


def test_create_success(base_model, mock_db_connection):

    base_model.data = {"column1": "value1", "column2": "value2"}
    expected_result = 1
    mock_db_connection.cursor().__enter__().rowcount = expected_result

    result = base_model.create()

    assert result == expected_result
    mock_db_connection.commit.assert_called_once()
    mock_db_connection.cursor().__enter__().execute.assert_called_once()


def test_create_failure(base_model, mock_db_connection):

    base_model.data = {"column1": "value1", "column2": "value2"}

    mock_db_connection.cursor().__enter__().execute.side_effect = Exception("Test exception")

    result = base_model.create()

    assert result is None
    mock_db_connection.rollback.assert_called_once()


def test_read_success(base_model, mock_db_connection):

    base_model.fields = ["column1", "column2"]
    expected_result = [("value1", "value2"), ("value3", "value4")]

    mock_db_connection.cursor().__enter__().fetchall.return_value = expected_result

    result = base_model.read()

    assert result == expected_result
    mock_db_connection.cursor().__enter__().execute.assert_called_once()


def test_read_failure(base_model, mock_db_connection):

    mock_db_connection.cursor().__enter__().execute.side_effect = Exception("Test exception")

    result = base_model.read()

    assert result is None


def test_update_success(base_model, mock_db_connection):

    expected_result = 2

    base_model.data = {"column1": "value1", "column2": "value2"}
    base_model.conditions = {"column3": "value3", "column4": "value4"}

    mock_db_connection.cursor().__enter__().rowcount = expected_result

    result = base_model.update()

    assert result == expected_result
    mock_db_connection.commit.assert_called_once()
    mock_db_connection.cursor().__enter__().execute.assert_called_once()


def test_update_failure(base_model, mock_db_connection):

    base_model.data = {"column1": "value1", "column2": "value2"}
    base_model.conditions = {"column3": "value3", "column4": "value4"}

    mock_db_connection.cursor().__enter__().execute.side_effect = Exception("Test exception")

    result = base_model.update()

    assert result is None
    mock_db_connection.rollback.assert_called_once()


def test_delete_success(base_model, mock_db_connection):

    expected_result = 3

    base_model.conditions = {"column1": "value2", "column3": "value4"}

    mock_db_connection.cursor().__enter__().rowcount = expected_result

    result = base_model.delete()

    assert result == expected_result
    mock_db_connection.commit.assert_called_once()
    mock_db_connection.cursor().__enter__().execute.assert_called_once()


def test_delete_failure(base_model, mock_db_connection):

    base_model.conditions = {"column1": "value2", "column3": "value4"}

    mock_db_connection.cursor().__enter__().execute.side_effect = Exception("Test exception")

    result = base_model.delete()

    assert result is None
    mock_db_connection.rollback.assert_called_once()
