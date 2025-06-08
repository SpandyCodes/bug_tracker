import unittest
import tempfile
import os
import sqlite3
from app import create_app
from config import DATABASE_PATH

class BugApiTestCase(unittest.TestCase):
    def setUp(self):
        # Create a temporary DB file
        self.db_fd, self.temp_db = tempfile.mkstemp()
        os.close(self.db_fd)

        # Patch config for the test
        import config
        config.DATABASE_PATH = self.temp_db

        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.temp_db

        self.client = self.app.test_client()

        # Create tables and insert test data
        conn = sqlite3.connect(self.temp_db)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        );
        ''')

        cursor.execute('''
        CREATE TABLE bugs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'open',
            progress INTEGER NOT NULL DEFAULT 0,
            assigned_to INTEGER,
            comments TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (assigned_to) REFERENCES users(id)
        );
        ''')

        # Insert admin user
        cursor.execute("INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
                       ("admin", "admin@example.com", "hashedpassword", "admin"))
        # Insert normal user
        cursor.execute("INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
                       ("user1", "user1@example.com", "hashedpassword", "user"))
        conn.commit()
        conn.close()

    def tearDown(self):
        os.remove(self.temp_db)

    def login(self, username, password='testpass'):
        return self.client.post('/auth/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_create_bug_unauthenticated(self):
        # Should redirect to login because not logged in
        response = self.client.post('/api/bugs', json={
            'title': 'Test Bug',
            'description': 'Bug description'
        })
        self.assertEqual(response.status_code, 401)

    def test_create_bug_as_admin(self):
        self.login('admin', 'hashedpassword')  # assuming password hash check not enforced in tests

        response = self.client.post('/api/bugs', json={
            'title': 'Test Bug',
            'description': 'Bug description'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Test Bug', response.data)

    def test_get_bugs(self):
        self.login('admin', 'hashedpassword')

        # Create a bug first
        self.client.post('/api/bugs', json={
            'title': 'Bug1',
            'description': 'Desc1'
        })

        response = self.client.get('/api/bugs')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bug1', response.data)

    def test_assign_bug(self):
        self.login('admin', 'hashedpassword')

        # Create bug
        response = self.client.post('/api/bugs', json={
            'title': 'Assign Bug',
            'description': 'Assign bug description'
        })
        bug = response.get_json()

        # Assign bug to user1
        response = self.client.put(f"/api/bugs/{bug['id']}/assign", json={
            'assigned_to': 2  # user1's id
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bug assigned successfully', response.data)

    def test_update_progress(self):
        self.login('user1', 'hashedpassword')

        # Admin creates a bug and assigns to user1
        self.login('admin', 'hashedpassword')
        response = self.client.post('/api/bugs', json={
            'title': 'Progress Bug',
            'description': 'Progress description'
        })
        bug = response.get_json()
        self.client.put(f"/api/bugs/{bug['id']}/assign", json={'assigned_to': 2})

        self.login('user1', 'hashedpassword')
        # User1 updates progress
        response = self.client.put(f"/api/bugs/{bug['id']}/progress", json={
            'progress': 50,
            'comments': 'Halfway done'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Progress updated successfully', response.data)

if __name__ == '__main__':
    unittest.main()
