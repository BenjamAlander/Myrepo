import os
import sqlite3

# Oletustietokannan polku, jos ympäristömuuttujaa ei ole asetettu
DEFAULT_DB_PATH = "/app/docker/config.db"

def initialize_db():
    """
    Luo tietokannan ja tarvittavat taulut.
    Polku haetaan DB_PATH-ympäristömuuttujasta tai käytetään oletusarvoa.
    """
    # Haetaan tietokannan polku ympäristömuuttujasta
    db_path = os.getenv("DB_PATH", DEFAULT_DB_PATH)
    print("[Debug] Using database path:", db_path)

    # Korvasin kovakoodatun polun db_path ympäristömuuttujalla, muuten testeissä tulee käyttäjäoikeusongelma. TÅ



    # Varmistetaan, että tietokannan hakemisto on olemassa
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Luodaan taulu, jos sitä ei ole
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configurations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id TEXT NOT NULL UNIQUE,
        token TEXT NOT NULL,
        last_checked TEXT DEFAULT NULL
    )
    """)

    # Tarkistetaan ja lisätään `last_checked`-sarake, jos sitä ei ole
    cursor.execute("PRAGMA table_info(configurations)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "last_checked" not in columns:
        cursor.execute("ALTER TABLE configurations ADD COLUMN last_checked TEXT")
        print("[Debug] Added column 'last_checked' to the database.")
    
    conn.commit()
    conn.close()
    print("[Debug] Database initialized successfully.")

if __name__ == "__main__":
    initialize_db()
