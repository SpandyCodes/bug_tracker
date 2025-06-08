import unittest
from app import create_app
from models.user import User
from config import DATABASE_PATH
import os
import tempfile
import sqlite3

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file
        self.db_fd, self.temp_db = tempfile.mkstemp()
        os.close(self.db_fd)  # Close fd so SQLite can use it

        # Patch DATABASE_PATH to use temporary DB
        from config import BASE_DIR
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.temp_db

        # Override config DATABASE_PATH for raw sqlite connections in models
        import config
        config.DATABASE_PATH = self.temp_db

        self.client = self.app.test_client()

        # Create tables in temp DB
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
        conn.commit()
        conn.close()

    def tearDown(self):
        # Remove the temporary database file
        os.remove(self.temp_db)

    def test_register_login_logout(self):
        # Register new user
        response = self.client.post('/auth/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass',
            'confirm_password': 'testpass'
        }, follow_redirects=True)
        self.assertIn(b'Registration successful', response.data)

        # Login with correct credentials
        response = self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'testpass'
        }, follow_redirects=True)
        self.assertIn(b'Dashboard', response.data)

        # Logout
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_login_invalid_user(self):
        response = self.client.post('/auth/login', data={
            'username': 'nonexistent',
            'password': 'wrongpass'
        }, follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)

    def test_register_password_mismatch(self):
        response = self.client.post('/auth/register', data={
            'username': 'user2',
            'email': 'user2@example.com',
            'password': 'pass1',
            'confirm_password': 'pass2'
        })
        self.assertIn(b'Passwords do not match', response.data)

if __name__ == '__main__':
    unittest.main()
