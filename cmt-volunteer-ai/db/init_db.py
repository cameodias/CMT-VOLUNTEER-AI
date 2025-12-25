from db.models import get_connection

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        city TEXT,
        join_date TEXT,
        bio TEXT,
        processed_at TEXT,
        status TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER,
        skill TEXT,
        FOREIGN KEY(member_id) REFERENCES members(id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS personas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER,
        persona TEXT,
        confidence REAL,
        version INTEGER,
        FOREIGN KEY(member_id) REFERENCES members(id)
    )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
