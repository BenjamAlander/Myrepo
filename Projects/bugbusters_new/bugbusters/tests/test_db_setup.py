# app/tests/test_db_setup.py

# Suorittaminen:
# Siirry oikeaan hakemistoon: cd ../Projekti4/bugbusters/tests
# Suorita testit komennolla: pytest -s test_db_setup.py

# Lisätään projektin juurihakemisto moduulipolkuun
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sqlite3
import pytest
from app.db_setup import initialize_db

# Testitietokannan sijainti
TEST_DB_PATH = "/tmp/test_config.db"

@pytest.fixture(scope="function")
def test_db():
    """
    Fixtuuri, joka asettaa ympäristömuuttujan testitietokantaa varten
    ja varmistaa, että tietokanta poistetaan ennen ja jälkeen testin.
    """
    os.environ["DB_PATH"] = TEST_DB_PATH
    print("\n[Fixture] Setting DB_PATH to:", TEST_DB_PATH)

    # Poistetaan testitietokanta, jos se on olemassa
    if os.path.exists(TEST_DB_PATH):
        print("[Fixture] Removing existing test database.")
        os.remove(TEST_DB_PATH)

    yield  # Palautetaan kontrolli testille

    # Poistetaan testitietokanta testin jälkeen
    if os.path.exists(TEST_DB_PATH):
        print("[Fixture] Cleaning up test database.")
        os.remove(TEST_DB_PATH)


def test_initialize_db_creates_database_and_table(test_db):
    """
    Testaa, että initialize_db-funktio luo tietokannan ja tarvittavat taulut.
    """
    print("\n[Test] Calling initialize_db to create the database and table.")
    initialize_db()

    # Tarkistetaan, että tietokanta on luotu
    assert os.path.exists(TEST_DB_PATH), "[Test] Database file was not created!"
    print("[Test] Database file created successfully:", TEST_DB_PATH)

    # Tarkistetaan, että taulu 'configurations' on luotu
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    print("[Test] Verifying the 'configurations' table exists in the database.")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='configurations';")
    result = cursor.fetchone()
    conn.close()

    # Varmistetaan, että taulu löytyy ja nimi on oikein
    assert result is not None, "[Test] Table 'configurations' does not exist!"
    assert result[0] == "configurations", "[Test] Table name is incorrect!"
    print("[Test] Table 'configurations' verified successfully.")
