import pytest
import sqlite3
from unittest.mock import patch

# Polku testitietokantaan
DB_PATH = "/tmp/test_config.db"

@pytest.fixture
def test_db():
    """
    Luo testitietokanta ja alustaa sen ohjelman oletusrakenteen mukaisesti.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Poistetaan vanha taulu ja luodaan uusi
    cursor.execute("DROP TABLE IF EXISTS configurations")
    cursor.execute(
        """
        CREATE TABLE configurations (
            id INTEGER PRIMARY KEY,
            project_id TEXT,
            token TEXT,
            last_checked TEXT
        )
        """
    )
    conn.commit()
    yield conn  # Palautetaan tietokantayhteys testejä varten
    conn.close()

@pytest.fixture
def mock_gitlab_api():
    """
    Mockaa kaikki GitLab API -pyynnöt.
    """
    with patch("requests.get") as mock_get, patch("requests.put") as mock_put, patch("requests.post") as mock_post:
        yield mock_get, mock_put, mock_post

@pytest.fixture
def client():
    """
    Palauttaa Flask-sovelluksen testiasiakkaan.
    """
    from app.service import app
    app.config["TESTING"] = True
    app.config["DATABASE"] = DB_PATH
    with app.test_client() as client:
        yield client