from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from services.bug_manager import BugManager

bug_blueprint = Blueprint('bug_api', __name__)
bug_manager = BugManager()

@bug_blueprint.route('/bugs', methods=['GET'])
@login_required
def get_bugs():
    bugs = bug_manager.get_bugs_for_user(current_user)
    bugs_data = []
    for b in bugs:
        bugs_data.append({
            'id': b.id,
            'title': b.title,
            'description': b.description,
            'status': b.status,
            'progress': b.progress,
            'comments': b.comments,
            'created_by': b.creator.username,
            'assigned_to': b.assignee.username if b.assignee else None,
            'created_at': b.created_at.isoformat(),
            'updated_at': b.updated_at.isoformat()
        })
    return jsonify(bugs_data), 200

@bug_blueprint.route('/bugs/<int:bug_id>/assign', methods=['POST'])
@login_required
def assign_bug(bug_id):
    if not current_user.is_admin():
        return jsonify({'error': 'Permission denied'}), 403
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
    user = bug_manager.assign_bug(bug_id, user_id)
    if not user:
        return jsonify({'error': 'Bug or User not found'}), 404
    return jsonify({'message': f'Bug assigned to {user.username}'}), 200

@bug_blueprint.route('/bugs/<int:bug_id>/unassign', methods=['POST'])
@login_required
def unassign_bug(bug_id):
    if not current_user.is_admin():
        return jsonify({'error': 'Permission denied'}), 403
    success = bug_manager.unassign_bug(bug_id)
    if not success:
        return jsonify({'error': 'Bug not found'}), 404
    return jsonify({'message': 'Bug unassigned'}), 200

@bug_blueprint.route('/bugs/<int:bug_id>/progress', methods=['PUT'])
@login_required
def update_progress(bug_id):
    bug = bug_manager.get_bug_by_id(bug_id)
    if not bug:
        return jsonify({'error': 'Bug not found'}), 404
    # Only assignee or admin can update progress
    if bug.assignee_id != current_user.id and not current_user.is_admin():
        return jsonify({'error': 'Permission denied'}), 403
    data = request.json
    progress = data.get('progress')
    comments = data.get('comments', '')
    if progress is None:
        return jsonify({'error': 'progress value required'}), 400
    bug_manager.update_progress_and_comments(bug_id, progress, comments)
    return jsonify({'message': 'Progress updated'}), 200
