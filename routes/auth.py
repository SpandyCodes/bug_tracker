from flask import Blueprint, jsonify, request, session
from models.user import User
from functools import wraps

auth_bp = Blueprint('auth_bp', __name__)

# Helper decorator for login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Helper decorator for admin required
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        user = User.get_by_id(user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Forbidden, admin only'}), 403
        return f(*args, **kwargs)
    return decorated_function

# API: Get current logged-in user info
@auth_bp.route('/api/userinfo', methods=['GET'])
@login_required
def api_userinfo():
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({
        'id': user.id,
        'username': user.username,
        'role': user.role
    })

# API: Get all users (admin only)
@auth_bp.route('/api/users', methods=['GET'])
@login_required
@admin_required
def api_get_users():
    users = User.get_all_users()
    users_list = [{'id': u.id, 'username': u.username} for u in users]
    return jsonify(users_list)

# POST logout route for AJAX logout
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})
