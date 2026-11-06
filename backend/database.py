
import sqlite3
from config.settings import DATABASE_PATH
import os

# Ensure database directory exists
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    # Complaints table
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
    conn.close()


def create_complaint(
    ticket_id,
    description,
    location,
    student_name=None
):
    conn = get_connection()
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
    conn.close()


def get_all_complaints():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM complaints
        ORDER BY created_at DESC
    """)

    complaints = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return complaints


def update_complaint(ticket_id, category, priority, department):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE complaints
        SET category = ?,
            priority = ?,
            department = ?
        WHERE ticket_id = ?
    """, (category, priority, department, ticket_id))

    conn.commit()
    conn.close()
