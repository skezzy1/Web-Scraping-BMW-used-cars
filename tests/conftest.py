import sqlite3
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_bmw_cars.db"

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE cars (
            registration TEXT,
            model TEXT,
            fuel TEXT,
            transmission TEXT,
            price REAL
        )
    """)
    cursor.executemany(
        "INSERT INTO cars VALUES (?, ?, ?, ?, ?)",
        [
            ("AA0001", "X5", "Diesel", "Auto", 55000.0),
            ("AA0002", "3 Series", "Petrol", "Manual", 25000.0),
        ],
    )
    conn.commit()
    conn.close()

    return str(db_file)


@pytest.fixture
def client(temp_db):
    with patch("app.main.DB_PATH", temp_db):
        with TestClient(app) as c:
            yield c
