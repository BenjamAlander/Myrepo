import os
import sqlite3

# Määritetään tietokannan polku Docker-kontin app-hakemistossa
db_path = "/app/docker/config.db"

def initialize_db():
    # Varmistetaan, että tietokannan hakemisto on olemassa
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS configurations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id TEXT NOT NULL UNIQUE,
            token TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()