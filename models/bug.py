import sqlite3
from config import DATABASE_PATH
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class Bug:
    def __init__(self, id, title, description, status, progress, assigned_to, comments, created_at, updated_at):
        self.id = id
        self.title = title
        self.description = description
        self.status = status            # e.g. "open", "in_progress", "closed"
        self.progress = progress        # integer 0-100 percent
        self.assigned_to = assigned_to  # user id or None
        self.comments = comments        # string or JSON string for now
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(title, description, assigned_to=None):
        now = datetime.utcnow().isoformat()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bugs (title, description, status, progress, assigned_to, comments, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (title, description, "open", 0, assigned_to, "", now, now)
        )
        conn.commit()
        bug_id = cursor.lastrowid
        conn.close()
        return Bug.get_by_id(bug_id)

    @staticmethod
    def get_by_id(bug_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bugs WHERE id = ?", (bug_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Bug(
                row['id'], row['title'], row['description'], row['status'],
                row['progress'], row['assigned_to'], row['comments'],
                row['created_at'], row['updated_at']
            )
        return None

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bugs ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [Bug(
            row['id'], row['title'], row['description'], row['status'],
            row['progress'], row['assigned_to'], row['comments'],
            row['created_at'], row['updated_at']
        ) for row in rows]

    @staticmethod
    def get_by_assigned_user(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bugs WHERE assigned_to = ? ORDER BY created_at DESC", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [Bug(
            row['id'], row['title'], row['description'], row['status'],
            row['progress'], row['assigned_to'], row['comments'],
            row['created_at'], row['updated_at']
        ) for row in rows]

    def update_progress(self, progress, comments=None):
        self.progress = progress
        if comments is not None:
            self.comments = comments
        # Update status based on progress
        self.status = "closed" if progress == 100 else ("in_progress" if progress > 0 else "open")
        self.updated_at = datetime.utcnow().isoformat()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE bugs SET progress = ?, comments = ?, status = ?, updated_at = ? WHERE id = ?",
            (self.progress, self.comments, self.status, self.updated_at, self.id)
        )
        conn.commit()
        conn.close()

    def assign_to_user(self, user_id):
        self.assigned_to = user_id
        self.updated_at = datetime.utcnow().isoformat()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE bugs SET assigned_to = ?, updated_at = ? WHERE id = ?",
            (user_id, self.updated_at, self.id)
        )
        conn.commit()
        conn.close()

    def remove_assignment(self):
        self.assigned_to = None
        self.updated_at = datetime.utcnow().isoformat()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE bugs SET assigned_to = NULL, updated_at = ? WHERE id = ?",
            (self.updated_at, self.id)
        )
        conn.commit()
        conn.close()
