
# ✅ Project Specification: Bug Tracker (Flask + OOP + REST API + Bootstrap)

## 🎯 Objective:
Build a complete **Bug Tracker Web App** using **Flask**, designed to demonstrate **Object-Oriented Programming (OOP)** principles, web development skills, RESTful APIs, role-based access, testing, and deployment readiness (e.g., **Vercel**).

---

## 📁 Project Directory Structure
```
bug_tracker/
├── app.py                         # Main Flask app
├── config.py                      # Configs (SECRET_KEY, DB)
├── setup_db.py                    # DB creation & sample seed data
├── models/
│   ├── __init__.py                # SQLAlchemy init
│   ├── user.py                    # User model (OOP)
│   └── bug.py                     # Bug model (OOP)
├── services/
│   └── bug_manager.py             # Business logic layer
├── routes/
│   ├── auth.py                    # Register/Login/Logout
│   └── bug_api.py                 # RESTful API for bugs
├── templates/
│   ├── base.html                  # Shared layout (Bootstrap)
│   ├── login.html                 # Login form
│   ├── register.html              # Register form
│   ├── dashboard.html             # Bugs overview (admin & users)
│   └── bug_detail.html            # View/Update bug progress
├── static/
│   └── style.css                  # Optional styling
├── tests/
│   ├── test_auth.py               # Auth unit tests
│   └── test_bug_api.py            # Bug API tests
├── requirements.txt               # Python dependencies
└── vercel.json                    # For Vercel deployment
```

---

## 👤 User Roles

### 🧑 Admin:
- Assign bugs to users
- View all bugs & assignees
- Modify bug details
- Unassign/reassign bugs
- Full access to all routes

### 👨‍💻 Regular User:
- View bugs assigned to them
- Add progress (0–100%)
- Comment on bugs
- Cannot assign or delete bugs

---

## ⚙️ Functional Requirements

### 🔐 Authentication:
- Register (email, username, password)
- Login/Logout (via Flask-Login)
- Passwords hashed using `Werkzeug`
- Admins detected via `is_admin=True` flag

---

### 🐞 Bug Operations:
- Create/Edit/Delete bugs (admin)
- View all/assigned bugs
- Update progress (% done)
- Add bug comments
- Filter bugs by:
  - Severity (Low, Medium, High)
  - Assigned user
  - Status (Open, In Progress, Done)

---

### 🌐 RESTful API (routes/bug_api.py):
- `GET /api/bugs`: List all bugs
- `GET /api/bugs/<id>`: Get single bug
- `POST /api/bugs`: Create new bug
- `PUT /api/bugs/<id>`: Update progress/comments
- `DELETE /api/bugs/<id>`: Delete bug
- `POST /api/assign/<bug_id>`: Assign a bug to user

---

## 🗄️ Database Models (SQLAlchemy)

### `User`
- `id`, `username`, `email`, `password_hash`, `is_admin`
- Relationship: `assigned_bugs`

### `Bug`
- `id`, `title`, `description`, `severity`, `status`
- `assigned_to`, `progress`, `comments`

---

## 📦 Dependencies (`requirements.txt`)
```
Flask
Flask-SQLAlchemy
Flask-Login
Werkzeug
pytest
```

---

## 🧪 Unit Tests
- Auth Tests: Login, register
- Bug API Tests: CRUD + filters
- Location: `/tests`

---

## 🛠️ Vercel Deployment

### `vercel.json`
```json
{
  "builds": [{ "src": "app.py", "use": "@vercel/python" }],
  "routes": [{ "src": "/(.*)", "dest": "app.py" }]
}
```

---

## 🧰 Sample Data with `setup_db.py`

This script must:
- Drop/create all tables
- Create:
  - Admin user
  - 3 regular users
  - 4 sample bugs (some assigned)
- Use `generate_password_hash()` for secure credentials

### Sample Accounts:
| Role   | Username | Email              | Password   |
|--------|----------|--------------------|------------|
| Admin  | admin    | admin@example.com  | `admin123` |
| User 1 | alice    | alice@example.com  | `alice123` |
| User 2 | bob      | bob@example.com    | `bob123`   |
| User 3 | carol    | carol@example.com  | `carol123` |

---

## 💻 Run Locally (Windows / Mac / Linux)

```bash
# Step 1: Clone project
cd bug_tracker

# Step 2: Create virtual environment
python -m venv bug_env
bug_env\Scripts\activate      # Windows
# source bug_env/bin/activate  # Mac/Linux

# Step 3: Install requirements
pip install -r requirements.txt

# Step 4: Initialize DB + Sample Data
python setup_db.py

# Step 5: Run the app
python app.py
```
