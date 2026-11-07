
import sqlite3
import os

from config.settings import DATABASE_PATH


# Ensure database directory exists
db_dir = os.path.dirname(DATABASE_PATH)

if db_dir:
    os.makedirs(db_dir, exist_ok=True)


def get_connection():
    """Create and return a database connection."""

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row

    return conn


def initialize_database():
    """Create the complaints table if it does not exist."""

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT UNIQUE,
                student_name TEXT,
                description TEXT NOT NULL,
                location TEXT NOT NULL,
                category TEXT,
                priority TEXT,
                department TEXT,
                status TEXT DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()

        print("[Database] Database initialized successfully.", flush=True)

    except sqlite3.Error as e:
        conn.rollback()
        print(f"[Database ERROR] {e}", flush=True)
        raise

    finally:
        conn.close()


def create_complaint(
    ticket_id,
    description,
    location,
    student_name=None
):
    """Insert a new complaint into the database."""

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO complaints (
                ticket_id,
                student_name,
                description,
                location
            )
            VALUES (?, ?, ?, ?)
        """, (
            ticket_id,
            student_name,
            description,
            location
        ))

        conn.commit()

        return True

    except sqlite3.Error as e:
        conn.rollback()
        print(f"[Database ERROR] {e}", flush=True)
        raise

    finally:
        conn.close()


def get_all_complaints():
    """Retrieve all complaints, newest first."""

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM complaints
            ORDER BY created_at DESC
        """)

        complaints = [
            dict(row) for row in cursor.fetchall()
        ]

        return complaints

    finally:
        conn.close()


def update_complaint(
    ticket_id,
    category,
    priority,
    department
):
    """Update category, priority, and department."""

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE complaints
            SET category = ?,
                priority = ?,
                department = ?
            WHERE ticket_id = ?
        """, (
            category,
            priority,
            department,
            ticket_id
        ))

        conn.commit()

        return cursor.rowcount > 0

    except sqlite3.Error as e:
        conn.rollback()
        print(f"[Database ERROR] {e}", flush=True)
        raise

    finally:
        conn.close()
